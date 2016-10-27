from __future__ import unicode_literals

from django.db import models

# Create your models here.


class JenkinsProject(models.Model):
    name = models.CharField(max_length=100)


class JenkinsJob(models.Model):
    project = models.ForeignKey(JenkinsProject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    execution_id = models.CharField(max_length=100)


class JenkinsTestSuite(models.Model):
    job = models.ForeignKey(JenkinsJob, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class JenkinsTestCase(models.Model):
    suite = models.ForeignKey(JenkinsTestSuite, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    total_actions = models.IntegerField()
    total_conditions = models.IntegerField()


class JenkinsTestBox(models.Model):
    box_type = models.CharField(max_length=3)
    unit_address = models.CharField(max_length=50)
    ipaddress = models.GenericIPAddressField()

class JenkinsResults(models.Model):
    JOB_RESULTS = (('PAAS', 'PAAS'),
                   ('FAIL', 'FAIL'))

    case = models.ForeignKey(JenkinsTestCase, on_delete=models.CASCADE)
    box = models.ForeignKey(JenkinsTestBox, on_delete=models.CASCADE,
            blank=True,
            null=True)
    result_date = models.DateTimeField('date')
    tester = models.CharField(max_length=100)
    pass_numbers = models.IntegerField()
    fail_numbers = models.IntegerField()
    result = models.CharField(max_length=4,
                              choices=JOB_RESULTS,
                              default=JOB_RESULTS[0][0])
    execution_time = models.IntegerField()

