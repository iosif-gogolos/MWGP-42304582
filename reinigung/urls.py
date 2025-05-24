from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('aufgabe-abhaken/', views.aufgabe_abhaken, name='aufgabe_abhaken'),
    path('putztag-beenden/', views.putztag_beenden, name='putztag_beenden'),
    path('admin-welcome-dismiss/', views.admin_welcome_dismiss, name='admin_welcome_dismiss'),
]

