from carpool.serializers import RoomIDSerializer
from PayUp.responses import POST_REQUEST_ERRORS
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from users.selectors import get_uid_from_token
from users.utils import get_token

from .selectors import get_active_session_data
from .serializers import (CreateActiveSessionSerializer,
                          StartActiveSessionSerializer, LeaveActiveSessionSerializer,
                          EndSessionSerializer, TestSerializer)
from .services import ( join_active_session, start_active_session, end_active_session, leave_active_session )

from .utils import start_drive_notif

class StartActiveSession(GenericAPIView):
    
    serializer_class = CreateActiveSessionSerializer

    def post(self, request, *args, **kwargs):
        user_id = get_uid_from_token(get_token(request))
        if user_id:

            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try:
                    data = serialized.validated_data
                    r = start_active_session(data, user_id)
                    return Response(r, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__.upper(), "MESSAGE": str(e)}, status=status.HTTP_409_CONFLICT)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)


class JoinActiveSession(GenericAPIView):
    
    serializer_class = StartActiveSessionSerializer

    def post(self, request, *args, **kwargs):
        user_id = get_uid_from_token(get_token(request))
        if user_id:
            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try:
                    data = serialized.validated_data
                    r = join_active_session(data, user_id)
                    return Response(r, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__.upper(), "MESSAGE": str(e)}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)


class GetActiveSessionData(GenericAPIView):
    
    serializer_class = RoomIDSerializer

    def post(self, request, *args, **kwargs):
        user_id = get_uid_from_token(get_token(request))
        if user_id:
            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try:
                    data = serialized.validated_data
                    r = get_active_session_data(data['room_id'], user_id)
                    return Response(r, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__.upper(), "MESSAGE": str(e)}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)

class LeaveActiveSession(GenericAPIView):
    
    serializer_class = LeaveActiveSessionSerializer

    def post(self, request, *args, **kwargs):
        user_id = get_uid_from_token(get_token(request))
        if user_id:
            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try:
                    data = serialized.validated_data
                    r = leave_active_session(data, user_id)
                    return Response(r, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__.upper(), "MESSAGE": str(e)}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)


class EndActiveSession(GenericAPIView):
    
    serializer_class = EndSessionSerializer

    def post(self, request, *args, **kwargs):
        user_id = get_uid_from_token(get_token(request))
        if user_id:
            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try:
                    data = serialized.validated_data
                    r = end_active_session(data, user_id)
                    return Response(r, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__.upper(), "MESSAGE": str(e)}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)


class TestView(GenericAPIView):
    
    serializer_class = RoomIDSerializer

    def post(self, request, *args, **kwargs):

        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid():
            try:
                data = serialized.validated_data
                r = start_drive_notif(**data)
                return Response(r, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'ERROR': type(e).__name__.upper(), "MESSAGE": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

