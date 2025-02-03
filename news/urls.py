from django.urls import path
from . import views

urlpatterns = [
    path('', views.issue_list, name='issue_list'),
    path('issue/<int:pk>/', views.issue_detail, name='issue_detail'),
]
