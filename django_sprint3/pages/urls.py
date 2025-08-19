from django.urls import path
from . import views

handler403 = 'pages.views.handler403'
handler404 = 'pages.views.handler404'
handler500 = 'pages.views.handler500'
CSRF_FAILURE_VIEW = 'pages.views.csrf_failure'

app_name = 'pages'

urlpatterns = [
    path('auth/login/', views.custom_login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/password/', views.change_password, name='change_password'),
    path('about/', views.about, name='about'),
    path('rules/', views.rules, name='rules'),
]

