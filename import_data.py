import sys
import csv
import datetime

import django
django.setup()

from jenkins_dashboard.models import (JenkinsProject, JenkinsJob,
                                      JenkinsTestSuite, JenkinsTestCase,
                                      JenkinsTestBox, JenkinsResults)


PROJECT_FIELDS = {'ProjectName': 'name'}
JOB_FIELDS = {'TestJobName': 'name',
              'ProjectName': 'project_id',
              'TestJobExecutionId': 'execution_id',
              }
SUIT_FIELDS = {'SuiteName': 'name',
               'TestJobName': 'job_id'}
CASE_FIELDS = {'TestCaseID': 'name',
               'SuiteName': 'suite_id',
               'Author': 'author',
               'TotalActions': 'total_actions',
               'TotalConditions': 'total_conditions'}
BOX_FIELDS = {'BoxType': 'box_type',
              'BoxUnitAddress': 'unit_address',
              'BoxIP': 'ipaddress'}
RESULT_FIELDS = {'idTestResult': 'id',
                 'BoxIP': 'box_id',
                 'TestCaseID': 'case_id',
                 'Date': 'result_date',
                 'Tester': 'tester',
                 'FailNumbers': 'fail_numbers',
                 'PassNumbers': 'pass_numbers',
                 'Result': 'result',
                 'ExecutionTime': 'execution_time'
                 }

project_data = {}
job_data = {}
suit_data = {}
case_data = {}
box_data = {}
result_data = {}

with open(sys.argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        project = {}
        job = {}
        suit = {}
        case = {}
        box = {}
        result = {}
        for key, value in row.iteritems():
            if key in PROJECT_FIELDS:
                project[PROJECT_FIELDS[key]] = value
            if key in JOB_FIELDS:
                job[JOB_FIELDS[key]] = value
            if key in SUIT_FIELDS:
                suit[SUIT_FIELDS[key]] = value
            if key in CASE_FIELDS:
                case[CASE_FIELDS[key]] = value
            if key in BOX_FIELDS:
                box[BOX_FIELDS[key]] = value
            if key in RESULT_FIELDS:
                result[RESULT_FIELDS[key]] = value
        project_data[project['name']] = project
        job_data[job['name']] = job
        suit_data[suit['name']] = suit
        case_data[case['name']] = case
        box_data[box['ipaddress']] = box
        result_data[result['id']] = result

for project_name, project in project_data.iteritems():
    p_obj = JenkinsProject(**project)
    p_obj.save()
    project_data[project_name] = p_obj.id

for job_name, job in job_data.iteritems():
    job['project_id'] = project_data[job['project_id']]

    j_obj = JenkinsJob(**job)
    j_obj.save()
    job_data[job_name] = j_obj.id

for suit_name, suite in suit_data.iteritems():
    suite['job_id'] = job_data[suite['job_id']]

    s_obj = JenkinsTestSuite(**suite)
    s_obj.save()

    suit_data[suit_name] = s_obj.id

for case_name, case in case_data.iteritems():
    case['suite_id'] = suit_data[case['suite_id']]

    c_obj = JenkinsTestCase(**case)
    c_obj.save()

    case_data[case_name] = c_obj.id

for box_name, box in box_data.iteritems():
    b_obj = JenkinsTestBox(**box)
    b_obj.save()
    box_data[box_name] = b_obj.id

for result in result_data.values():
    
    result['case_id'] = case_data[result['case_id']]
    result['box_id'] = box_data[result['box_id']]

    result['id'] = int(result['id'])
    result['result_date'] = \
            datetime.datetime.strptime(result['result_date'], '%m/%d/%Y %H:%S')

    r_obj = JenkinsResults(**result)
    r_obj.save()
