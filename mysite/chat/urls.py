from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("appeal&<str:appeal_id>/", views.appeal_chat, name="room"),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('create_of_appeal/', views.create_appeal, name='create'),
    path('deactivate_appeal/<int:appeal_id>', views.deactivate_appeal, name='deactivate'),
    path('user_appeals/', views.user_appeals, name='my_appeal'),
]