from django.urls import path, include
from .views import ( UserRegister, 
                     UserLogin,
                     GetUserData,
                     SetUserData,
                     SetAdditionalUserData,
                     GetAdditionalUserData,
                     UserTokenRefresh
                   )


urlpatterns = [

    path('register/', UserRegister.as_view()), # Refactor to include() later
    path('login/', UserLogin.as_view()),
    path('refreshtoken/', UserTokenRefresh.as_view()),
    path('getuserdata/', GetUserData.as_view()),
    path('setuserdata/', SetUserData.as_view()),
    path('setaddress/', SetAdditionalUserData.as_view()),
    path('getaddress/', GetAdditionalUserData.as_view()),
 
]