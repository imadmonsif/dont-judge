from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_room/', views.create_room, name='create_room'),
    path('join_room/<str:room_code>/', views.join_room, name='join_room'),
    path('room/<str:room_code>/', views.room, name='room'),  # Render room page
]
