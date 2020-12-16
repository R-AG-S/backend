from django.conf.urls import url
from rest_framework import permissions
from .views import ( CreateRoomView, RoomJoinView )

from django.urls import path, include

urlpatterns = [
   path('create_room', CreateRoomView.as_view()),
   path('join_room', RoomJoinView.as_view()),

]