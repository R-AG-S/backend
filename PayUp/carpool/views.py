from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from PayUp.responses import POST_REQUEST_ERRORS
from .serializers import RoomCreateSerializer
from .services import createroom
from rest_framework.views import APIView


class CreateRoomView(GenericAPIView):
    
    serializer_class = RoomCreateSerializer

    def post(self, request, *args, **kwargs):
        #token = get_token(request)
        #user_id = get_uid_from_token(token)
        user_id = True
        if user_id:

            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try: 
                    r = createroom(serialized.validated_data)
                    return Response({"ROOM_ID": r}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__}, status=status.HTTP_409_CONFLICT)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_400_BAD_REQUEST)


