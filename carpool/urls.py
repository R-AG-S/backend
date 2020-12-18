from django.conf.urls import url
from rest_framework import permissions
from .views import ( CreateRoomView, RoomJoinView, RoomDataView, GetAllRoomsOfUserID, GetAllRoomsOfUserData )

from django.urls import path, include

urlpatterns = [
   path('create_room', CreateRoomView.as_view(), name= "Create A New Room"),
   path('join_room', RoomJoinView.as_view(), name= "Join An Existing Room"),
   path('get_room_data', RoomDataView.as_view(), name= "Get Details of a Joined Room"),
   path('user_rooms/id', GetAllRoomsOfUserID.as_view(), name= "Get Room ID of User's Rooms"),
   path('user_rooms/data', GetAllRoomsOfUserData.as_view(), name= "Get Room Data of User's Rooms"),

]