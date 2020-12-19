from django.conf.urls import url
from .views import ( StartActiveSession, JoinActiveSession, GetActiveSessionData )
from django.urls import path, include

urlpatterns = [
   path('start_drive', StartActiveSession.as_view(), name= "Start an Active Carpool Session"),
   path('join_drive', JoinActiveSession.as_view(), name= "Join an Active Carpool Session"),
   path('active_session_data', GetActiveSessionData.as_view(), name= "Get data of an Active Carpool Session"),
]