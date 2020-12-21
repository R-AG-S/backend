from django.conf.urls import url
from django.urls import include, path

from .views import (EndActiveSession, GetActiveSessionData, JoinActiveSession,
                    StartActiveSession, LeaveActiveSession, TestView, GetDriveHistory)

urlpatterns = [
   path('start_drive', StartActiveSession.as_view(), name= "Start an Active Carpool Session"),
   path('join_drive', JoinActiveSession.as_view(), name= "Join an Active Carpool Session"),
   path('get_drive_data', GetActiveSessionData.as_view(), name= "Get data of an Active Carpool Session"),
   path('get_history', GetDriveHistory.as_view(), name= "Get data of Previous Carpool Sessions"),
   path('leave_drive', LeaveActiveSession.as_view(), name= "Leave an Active Carpool Session"),
   path('end_drive', EndActiveSession.as_view(), name= "End an Active Carpool Session"),

   path('debug', TestView.as_view(), name= "Testing Ping"),
]
