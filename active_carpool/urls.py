from django.conf.urls import url
from rest_framework import permissions
#from .views import ( CreateRoomView, RoomJoinView, RoomDataView )

from django.urls import path, include

urlpatterns = [
   path('start_drive', None, name= "Create A New Room"),


]