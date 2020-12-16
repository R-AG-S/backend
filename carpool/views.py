from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from PayUp.responses import POST_REQUEST_ERRORS
from .serializers import RoomCreateSerializer, RoomJoinSerializer 
from .services import createroom, joinroom
from rest_framework.views import APIView

from users.selectors import get_uid_from_token
from users.utils import get_token


class CreateRoomView(GenericAPIView):
    
    serializer_class = RoomCreateSerializer

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        user_id = get_uid_from_token(token)
        if user_id:

            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try:
                    data = serialized.validated_data
                    r = createroom(data, user_id)
                    return Response({"ROOM_ID": r}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__}, status=status.HTTP_409_CONFLICT)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)


class RoomJoinView(GenericAPIView):
    
    serializer_class = RoomJoinSerializer

    def post(self, request, *args, **kwargs):
        token = get_token(request)
        user_id = get_uid_from_token(token)
        if user_id:

            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try: 
                    room_id = serialized.validated_data['room_id']
                    r = joinroom(room_id, user_id)
                    return Response({"SUCCESS": r}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)

