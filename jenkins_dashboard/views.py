import uuid
import time

from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import (JenkinsProject, JenkinsJob,
                     JenkinsTestSuite, JenkinsTestCase,
                     JenkinsResults)

from jenkinsapi.jenkins import Jenkins

JOB_XML = '''<?xml version='1.0' encoding='UTF-8'?>
<project>
    <actions/>
    <description></description>
    <keepDependencies>false</keepDependencies>
    <properties/>
    <scm class="hudson.scm.NullSCM"/>
    <canRoam>true</canRoam>
    <disabled>false</disabled>
    <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
    <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
    <triggers/>
    <concurrentBuild>false</concurrentBuild>
    <builders>
        <hudson.tasks.Shell>
            <command>{0}</command>
        </hudson.tasks.Shell>
    </builders>
    <publishers/>
    <buildWrappers/>
</project>
'''

# Create your views here.

def index(request):
    '''
    Index view for jenkins dashboard
    '''
    passed = [JenkinsResults.objects.filter(result='PAAS').count()]
    failed = [JenkinsResults.objects.filter(result='FAIL').count()]

    xdata = [1]

    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " jobs"}}

    chartdata = {
        'x': xdata,
        'name1': 'Passed', 'y1': passed, 'extra1': extra_serie,
        'name2': 'Failed', 'y2': failed, 'extra2': extra_serie,
    }

    charttype = "multiBarChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata
    }

    return render(request, 'jenkins_dashboard/index.html', data)

def submit_job(request):
    server = Jenkins(settings.JENKINS_URL,
                     username=settings.JENKINS_USER,
                     password=settings.JENKINS_PASSWORD)


    job_uuid = str(uuid.uuid1())
    project_name = request.POST['firstname'] + '_' + job_uuid

    project = JenkinsProject(name=project_name)
    project.save()

    job = JenkinsJob(name=project_name + '_job',
                     execution_id=job_uuid,
                     project=project)
    job.save()

    test_suite = \
        JenkinsTestSuite(name=project_name + '_suite',
                         job=job)
    test_suite.save()

    test_case = \
        JenkinsTestCase(name=project_name + '_case',
                        author='test',
                        total_actions=0,
                        total_conditions=0,
                        suite=test_suite)
    test_case.save()

    command = ' '.join((request.POST['firstname'], request.POST['lastname']))

    new_job = server.create_job(project_name, JOB_XML.format(command))
    new_job.invoke()

    time.sleep(5)
    result_dict = \
        dict(result='FAIL',
             result_date=timezone.now(),
             execution_time=0,
             tester='test',
             fail_numbers=0,
             pass_numbers=0,
             case=test_case)

    if server[project_name].get_build_dict():
        build = server[project_name].get_build_metadata(1)

        result_dict['result'] = build.get_status()[:4]
        result_dict['result_date'] = build.get_timestamp(),
        result_dict['execution_time'] = build.get_duration()

    result = JenkinsResults(**result_dict)
    result.save()


    return HttpResponseRedirect(reverse('jenkins_dashboard:index'))
