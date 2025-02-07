from django.urls import path
from news import views

urlpatterns = [
    path('', views.issue_list, name='issue_list'),
    path('main/', views.main, name='main'),
    path('news/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('news/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('news/<int:pk>/react/', views.add_reaction, name='add_reaction'),
    path('create_news/', views.create_news, name='create_news'),
    path('latest/', views.latest, name='latest'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('login/', views.custom_login, name='custom-login'),
    path('login/', views.custom_login, name='login'),
    path('register/', views.register, name='register'),
]
