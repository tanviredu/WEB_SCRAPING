from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='home'),
    ## this path is form taking the post value
    path('main/process/',views.process,name='process')

]
