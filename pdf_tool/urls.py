from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('merge/', views.merge_pdf, name='merge_pdf'),
    path('extract/', views.extract_pdf, name='extract_pdf'),
    path('logs/', views.view_logs, name='view_logs'),
]
