from rest_framework.response import Response
from rest_framework import status

def get_token(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        return token
    except:
        return -1


