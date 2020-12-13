"""
        NOTE: REFER TO  viewsAPITable.txt for API response table and documentation.
"""
from .selectors import (
    sign_in_with_email_and_password, 
    get_uid_from_token,
    get_user_data_from_uid,
    obj_to_json,
    get_additional_user_data,
    firebase_refresh_token
    )
from .services import (
    create_firebase_user,
    firebase_custom_token_generator,
    update_firebase_user,
    set_addresss_user
    )
from .serializers import (
    UserSerializer, 
    UserEditSerializer,
    LoginInputSerializer,
    RefreshToken,
    CustomerInfoSerializer,
    )

from .utils import get_token
from PayUp.responses import POST_REQUEST_ERRORS

from PayUp.utils import ApiErrorsMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

#from users.models import User



class UserRegister(ApiErrorsMixin, GenericAPIView):

    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.data
            try:
                user_firebase = create_firebase_user(user)
                return Response({'SUCCESS': "USER_CREATED_SUCCESSFULLY"}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLogin(ApiErrorsMixin, GenericAPIView):

    serializer_class = LoginInputSerializer

    def post(self, request):
        email_pass = self.serializer_class(data=request.data)

        if email_pass.is_valid():

            response = sign_in_with_email_and_password(**email_pass.data)
        
            if response.status_code == 400:
                error_message = response.json()
                return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)
            elif response.status_code == 200:
                token = response.json()
                return Response(token, status=status.HTTP_200_OK)
            else:
                return Response({"ERROR": "FIREBASE_ERROR: "+  response.status_code}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(email_pass.errors, status=status.HTTP_400_BAD_REQUEST) 



class GetUserData(ApiErrorsMixin, GenericAPIView):

    def get(self, request):
        token = get_token(request)
        user_id = get_uid_from_token(token)

        if user_id != None:
            firebase_user = get_user_data_from_uid(uid = user_id)
            if firebase_user != None:
                json_payload = obj_to_json(firebase_user)
                return Response(json_payload, status=status.HTTP_200_OK)
            else:
                return Response({"ERROR": "USER_DOES_NOT_EXIST"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_400_BAD_REQUEST)
        



class SetUserData(ApiErrorsMixin, GenericAPIView):
    
    serializer_class = UserEditSerializer

    def post(self, request):
  
        token = get_token(request)
        token_uid = get_uid_from_token(token)
        if token_uid:
            userObject = self.serializer_class(request.data) 
            try:
                user = update_firebase_user(token_uid, userObject.data)
                return Response({"SUCCESS":"USER_DATA_SET"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_400_BAD_REQUEST)



class GetAdditionalUserData(ApiErrorsMixin, GenericAPIView):


    def get(self, request):
  
        token = get_token(request)
        token_uid = get_uid_from_token(token)
        if token_uid:
            
            try:
                r = get_additional_user_data(token_uid)
                json_payload = obj_to_json(r)
                return Response(json_payload, status=status.HTTP_200_OK)
            except:
                return Response(POST_REQUEST_ERRORS['DATABASE_TIMED_OUT'], status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_400_BAD_REQUEST)  



class SetAdditionalUserData(ApiErrorsMixin, GenericAPIView):
    
    serializer_class = CustomerInfoSerializer

    def post(self, request):
  
        token = get_token(request)
        token_uid = get_uid_from_token(token)
        if token_uid:
            
            address = self.serializer_class(request.data)
        
            try:
                r = set_addresss_user(token_uid, address.data)

                return Response({"SUCCESSFUL": "USER_DATA_SET"}, status=status.HTTP_201_CREATED)
            except:
                return Response(POST_REQUEST_ERRORS['DATABASE_TIMED_OUT'], status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_400_BAD_REQUEST)


class UserTokenRefresh(ApiErrorsMixin, GenericAPIView):

    serializer_class = RefreshToken

    def post(self, request):
        token = self.serializer_class(data=request.data)
        if token.is_valid():

            response = firebase_refresh_token(**token.data)
        
            if response.status_code == 400:
                error_message = response.json()
                return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)
            elif response.status_code == 200:
                token = response.json()
                return Response(token, status=status.HTTP_200_OK)
            else:
                return Response({"ERROR": "FIREBASE_ERROR: "+  response.status_code}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_400_BAD_REQUEST)