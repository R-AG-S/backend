from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from PayUp.responses import POST_REQUEST_ERRORS
from users.selectors import get_uid_from_token
from users.utils import get_token


from .serializers import RoomCreateSerializer, RoomIDSerializer 
from .services import createroom, joinroom
from .selectors import get_room_details_full, get_all_rooms_details_id, get_all_rooms_details_full




class CreateRoomView(GenericAPIView):
    
    serializer_class = RoomCreateSerializer

    def post(self, request, *args, **kwargs):
        user_id = get_uid_from_token(get_token(request))
        if user_id:

            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try:
                    data = serialized.validated_data
                    r = createroom(data, user_id)
                    return Response(r, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__, "MESSAGE": str(e)}, status=status.HTTP_409_CONFLICT)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)


class RoomJoinView(GenericAPIView):
    
    serializer_class = RoomIDSerializer

    def post(self, request, *args, **kwargs):

        user_id = get_uid_from_token(get_token(request))
        if user_id:

            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try: 
                    room_id = serialized.validated_data['room_id']
                    r = joinroom(room_id, user_id)
                    return Response({"Room_Data": r}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__, "MESSAGE": str(e)}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)



class RoomDataView(GenericAPIView):
    
    serializer_class = RoomIDSerializer

    def post(self, request, *args, **kwargs):

        user_id = get_uid_from_token(get_token(request))
        if user_id:
            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try: 
                    room_id = serialized.validated_data['room_id']
                    r = get_room_details_full(room_id, user_id)
                    return Response({"Room_Data": r}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__, "MESSAGE": str(e)}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)


class GetAllRoomsOfUserID(GenericAPIView):

    def get(self, request, *args, **kwargs):
        user_id = get_uid_from_token(get_token(request))
        if user_id:
            try: 
                r = get_all_rooms_details_id(user_id)
                return Response({"Rooms": r}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'ERROR': type(e).__name__, "MESSAGE": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)


class GetAllRoomsOfUserData(GenericAPIView):

    def get(self, request, *args, **kwargs):
        user_id = get_uid_from_token(get_token(request))
        if user_id:
            try: 
                r = get_all_rooms_details_full(user_id)
                return Response({"Rooms": r}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'ERROR': type(e).__name__, "MESSAGE": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)






