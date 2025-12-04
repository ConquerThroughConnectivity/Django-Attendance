
from django.urls import include, path
from attendance import views
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from attendance.views import  Chat, ChatConversation, ConversationChat, DeleteChat, DeleteChatConvo, ProfileOverview, TimeClockDelete, TimeClockIn, TimeClockOut, TimeClockDateView, TimeClockViewUser,   Usersinformation, getConversation, getToUserChat,  getUserChat, registerwithFacebook, registerwithGoogle, searchUser, updateUser


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/' ,views.users, name="users"),
    path('getusers/<str:pk>/' ,views.getusers, name="getusers"),
    path('login' ,views.login, name="login"),
    path('register', views.register, name="register"),
    path('deleteclock/<str:id>/', TimeClockDelete.as_view(), name="deleteclock"),
    path('viewUsers', Usersinformation.as_view(), name="viewUsers"),
    path('getclockinbydate/<str:userID>/<str:date>', TimeClockDateView.as_view(), name="getclockinbydate"),
    path('getuserclockinout/<str:userID>', TimeClockViewUser.as_view(), name="getuserclockinout"),
    path('clockIn', TimeClockIn.as_view(), name ="clockIn"),
    path('profileOverview/<str:id>', ProfileOverview.as_view(), name ="profileOverview"),
    path('chat', Chat.as_view(), name ="chat"),
    path('deletechat/<str:id>', DeleteChat.as_view(), name ="chat"),
    path('searchUser/<str:email>', searchUser.as_view(), name ="searchUser"),
    path('updateUser/<str:userid>', updateUser.as_view(), name ="updateUser"),
    path('getUserchat/<str:fromuserid>/<str:touserid>', getUserChat.as_view(), name ="getUserchat"),
    path('getConversation/<str:pk>', getConversation.as_view(), name ="getConversation"),
    path('addconversation', ChatConversation.as_view(), name ="Conversation"),
    path('registerwithGoogle', views.registerwithGoogle, name ="registerwithGoogle"),
    path('registerwithFacebook', views.registerwithFacebook, name ="registerwithFacebook"),
    path('ConversationChat/<str:id>', ConversationChat.as_view(), name ="ConversationChat"),
    path("DeleteConversation/<str:id>", DeleteChatConvo.as_view(), name ="DeleteConversation"),
    path('getToUserchat/<str:id>', getToUserChat.as_view(), name ="getchat"),
    path('clockOut/<str:id>', TimeClockOut.as_view(), name ="clockOut"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 
]






