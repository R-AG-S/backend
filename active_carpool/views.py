from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from PayUp.responses import POST_REQUEST_ERRORS
from users.selectors import get_uid_from_token
from users.utils import get_token

from .serializers import StartActiveSessionSerializer

class StartActiveSession(GenericAPIView):
    
    serializer_class = StartActiveSessionSerializer

    def post(self, request, *args, **kwargs):
        user_id = get_uid_from_token(get_token(request))
        if user_id:

            serialized = self.serializer_class(data=request.data)
            if serialized.is_valid():
                try:
                    data = serialized.validated_data
                    r = None
                    return Response(r, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'ERROR': type(e).__name__, "MESSAGE": str(e)}, status=status.HTTP_409_CONFLICT)
            else:
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_401_UNAUTHORIZED)