from django.contrib import admin
from django.urls import path
from . import views
from .api import register_api, login_api, logout_api, predict_api

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('predict/', views.predict, name='predict'),
    path('logout/', views.logout_view, name='logout'),
    
    # API endpoints
    path('api/register/', register_api, name='api_register'),
    path('api/login/', login_api, name='api_login'),
    path('api/logout/', logout_api, name='api_logout'),
    path('api/predict/', predict_api, name='api_predict'),
]