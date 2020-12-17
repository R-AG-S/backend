from django.urls import path, include
from .views import ( UserRegister, 
                     UserLogin,
                     GetUserData,
                     SetUserData,
                     GetUserCar,
                     SetUserCar,
                     UserTokenRefresh
                   )


urlpatterns = [

    path('register/', UserRegister.as_view()), # Refactor to include() later
    path('login/', UserLogin.as_view()),
    path('refresh_token/', UserTokenRefresh.as_view()),
    path('get_user_data/', GetUserData.as_view()),
    path('set_user_data/', SetUserData.as_view()),
    path('set_car_details/', SetUserCar.as_view()),
    path('get_car_details/', GetUserCar.as_view()),
 
]