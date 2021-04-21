from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='FERS-home'),
    path('report/', views.report_bug , name='FERS-report-bug'),
    path('predict/', views.predict , name='predict')
   ]
