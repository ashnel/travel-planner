from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^travels$', views.submit, name="my_submit"),
    url(r'logout$', views.logout),
    url(r'^add$', views.add, name="my_add"),
    url(r'^create$', views.create, name="my_create"),
    url(r'^travels/dashboard', views.dashboard, name="my_dash"),
    url(r'^destination/(?P<trip_id>\d+)$', views.view, name="my_view"),
    url(r'^join/(?P<trip_id>\d+)$', views.join, name="my_join"),
]