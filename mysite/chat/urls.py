from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("appeal<str:client_id>/", views.appeal_chat, name="room"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('create_of_appeal_for/', views.create_appeal, name='create')
]