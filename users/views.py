"""
        NOTE: REFER TO  viewsAPITable.txt for API response table and documentation.
"""
import json

from PayUp.responses import POST_REQUEST_ERRORS
from PayUp.utils import ApiErrorsMixin
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .selectors import (firebase_refresh_token, get_specific_details_of_user,
                        get_uid_from_token, get_user_data_from_uid,
                        obj_to_json, sign_in_with_email_and_password,
                        get_all_details_of_user, get_display_details)
from .serializers import (CustomerInfoSerializer, LoginInputSerializer,
                          RefreshToken, UserEditSerializer,
                          UserRegisterationSerializer, UserIDSerializer, NameAndDPSerializer)
from .services import (create_firebase_user, firebase_custom_token_generator,
                       set_car_of_user, set_name_and_dp_of_user, update_firebase_user, delete_car_of_user,
                        delete_car_of_user, add_device_token_to_user_table)
from .utils import get_token


class UserRegister(ApiErrorsMixin, GenericAPIView):

    serializer_class = UserRegisterationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            userdata = serializer.data
            try:
                user_firebase = create_firebase_user(userdata)
                if userdata['auto_login']:
                    response = sign_in_with_email_and_password(userdata['email'], userdata['password'])
                    if response.status_code == 400:
                        error_message = response.json()
                        return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)
                    elif response.status_code == 200:
                        token = response.json()
                        if 'device_registeration_token' in userdata:
                            token['user_data']= add_device_token_to_user_table(userdata['device_registeration_token'], token['localId'])
                        return Response(token, status=status.HTTP_201_CREATED)
                else:
                    return Response({"SUCCESS": "USER_CREATED_SUCCESSFULLY"}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLogin(ApiErrorsMixin, GenericAPIView):

    serializer_class = LoginInputSerializer

    def post(self, request):
        email_pass = self.serializer_class(data=request.data)

        if email_pass.is_valid():
            userdata = email_pass.validated_data
            response = sign_in_with_email_and_password(userdata['email'], userdata['password'])
        
            if response.status_code == 400:
                error_message = response.json()
                return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)
            elif response.status_code == 200:
                user_table = {}
                token = response.json()
                if 'device_registeration_token' in userdata:
                    token['user_data']= add_device_token_to_user_table(userdata['device_registeration_token'], token['localId'])
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
                json_payload = json.loads(json.dumps(firebase_user.__dict__, indent=4))
                return Response(json_payload['_data'], status=status.HTTP_200_OK)
            else:
                return Response({"ERROR": "USER_DOES_NOT_EXIST"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_400_BAD_REQUEST)


class GetAnyUsersDisplayData(ApiErrorsMixin, GenericAPIView):
    def get(self, request, user_id):
        try:
            print(user_id)
            data = get_display_details(user_id)
            print(data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"ERROR": str(e)}, status=status.HTTP_404_NOT_FOUND)


        



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



class GetUserExtraDetails(ApiErrorsMixin, GenericAPIView):

    def post(self, request):
        token = get_token(request)
        token_uid = get_uid_from_token(token)
        if token_uid:
            try:
                r = get_all_details_of_user(token_uid)
                return Response(r, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_400_BAD_REQUEST)  


class SetNameAndPic(ApiErrorsMixin, GenericAPIView):
    
    serializer_class = NameAndDPSerializer

    def post(self, request):
        token = get_token(request)
        token_uid = get_uid_from_token(token)
        if token_uid:
            car = self.serializer_class(request.data)
            try:
                r = set_name_and_dp_of_user(token_uid, car.data)
                return Response({"SUCCESSFUL": "USER_DATA_SET"}, status=status.HTTP_201_CREATED)
            except:
                return Response(POST_REQUEST_ERRORS['DATABASE_TIMED_OUT'], status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_400_BAD_REQUEST)


class GetUserCar(ApiErrorsMixin, GenericAPIView):
    serializer_class = UserIDSerializer
    def post(self, request):
        #token = get_token(request)
        #token_uid = get_uid_from_token(token)
        if True:
            data = self.serializer_class(request.data) 
            try:
                r = get_specific_details_of_user(data.data['user_id'], 'cars')
                return Response(r, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_400_BAD_REQUEST)  


class SetUserCar(ApiErrorsMixin, GenericAPIView):
    
    serializer_class = CustomerInfoSerializer

    def post(self, request):
  
        token = get_token(request)
        token_uid = get_uid_from_token(token)
        if token_uid:
            
            car = self.serializer_class(request.data)
        
            try:
                r = set_car_of_user(token_uid, car.data)

                return Response({"SUCCESSFUL": "USER_DATA_SET"}, status=status.HTTP_201_CREATED)
            except:
                return Response(POST_REQUEST_ERRORS['DATABASE_TIMED_OUT'], status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response(POST_REQUEST_ERRORS['INVALID_TOKEN'], status=status.HTTP_400_BAD_REQUEST)

class DeleteUserCar(ApiErrorsMixin, GenericAPIView):
    
    serializer_class = CustomerInfoSerializer

    def post(self, request):
  
        token = get_token(request)
        token_uid = get_uid_from_token(token)
        if token_uid:
            
            car = self.serializer_class(request.data)
        
            try:
                r = delete_car_of_user(token_uid, car.data)

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
