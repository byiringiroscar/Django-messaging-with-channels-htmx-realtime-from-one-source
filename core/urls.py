from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("user/<int:id>/", views.user_message, name="user_message"),
    path('auth/message', views.auth_message, name='auth_message')
]