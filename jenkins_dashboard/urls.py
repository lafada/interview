from django.conf.urls import url

from . import views

app_name = 'jenkins_dashboard'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit_job/$', views.submit_job, name='submit_job'),
]
