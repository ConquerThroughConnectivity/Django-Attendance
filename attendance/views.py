


from operator import is_
import profile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q
from attendance.serializers import LoginSerialize, SerializeChat, SerializeClockInOut, SerializeConversation, SerializeUser, Serializelogin
from attendance.models import  ChatModel, Conversation, LoginModel, TimeInOutClock, UserModel
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import User
from rest_framework.views import APIView
from datetime import date, datetime, time
from django.db.models.functions import Round
from django.db.models import F
from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import UserModel, Conversation
from .serializers import SerializeConversation




@api_view(['GET', 'POST'])
def users(request):
  if request.method == 'GET':
    users = UserModel.objects.all()
    serializer = SerializeUser(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  elif request.method == 'POST':
    serializer = SerializeUser(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getusers(request, pk):
    try:
      user = UserModel.objects.get(id = pk)
    except UserModel.DoesNotExist:
      return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'GET':
     serialize =SerializeUser(user)
    return Response(serialize.data, status=status.HTTP_200_OK)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def login(request):
     email = request.data.get('email')
     password = request.data.get('password')
     try:
         user = UserModel.objects.get(email=email)
         if user.check_password(password):
           tokens = get_tokens_for_user(user)
           return Response({
                "user": Serializelogin(user).data,
                "tokens": tokens,
            }, status=status.HTTP_200_OK)
         else:
          return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
     except UserModel.DoesNotExist:
          return Response({"error": "User not Found"}, status=status.HTTP_401_UNAUTHORIZED)
     


class Usersinformation(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request):
    user = UserModel.objects.all()
    serializer = SerializeUser(user, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

      

class TimeClockDelete(APIView):
    def post(self, request, id):
         try:
          time =TimeInOutClock.objects.filter(id =id)
         except time.DoesNotExist:
          return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)
         time.delete()
         return Response({'message': 'Clock deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class TimeClockOut(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, id):
        time_out = request.data.get('time_out')
        time_out_description = request.data.get('time_out_description')
        time_out_location = request.data.get('time_out_location')
        time =TimeInOutClock.objects.filter(id=id)
        for timeout in time:
          timeout.time_out =time_out
          timeout.time_out_description =time_out_description
          timeout.time_out_location =time_out_location
          time_format = "%I:%M %p"
          start_dt = datetime.strptime(timeout.time_in, time_format)
          end_dt = datetime.strptime(timeout.time_out, time_format) 
          timeout.hrs = end_dt - start_dt 
        #  timeout.hrs = timeout.hrs.total_seconds() / 3600
          timeout.save(update_fields=['time_out'])
          timeout.save(update_fields=['time_out_description'])
          timeout.save(update_fields=['time_out_location'])
          timeout.save(update_fields=['hrs'])
          serializer = SerializeClockInOut(time, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TimeClockIn(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request,):
    serializer = SerializeClockInOut(data=request.data)
    if serializer.is_valid():
       serializer.save()
       return Response(serializer.data, status=status.HTTP_200_OK)
    
  def get(self, request,):
        clockin = TimeInOutClock.objects.all()
        serializer = SerializeClockInOut(clockin, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

  
class TimeClockDateView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request, userID, date):
     try:  
      clockin = TimeInOutClock.objects.filter(userID=userID).filter(date=date)
      if not clockin.exists():
        serializer = SerializeClockInOut(clockin, many=True)
        return Response({"data":serializer.data})
      elif clockin is not None:
        serializer = SerializeClockInOut(clockin, many=True)
        return Response({"data":serializer.data},)
     except TimeInOutClock.DoesNotExist:
        return Response({"Error", "not Found"},)
   
 
class ProfileOverview(APIView):
     permission_classes = [IsAuthenticated]
     def get(self, req, id):
      user = UserModel.objects.filter(id=id)
      serializer = SerializeUser(user, many=True)
      clockin = TimeInOutClock.objects.filter(userID=id)
      clockinout = SerializeClockInOut(clockin, many=True)
      return Response({"user_data":serializer.data,"timeclock_data":clockinout.data})

class ConversationChat(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request, id):
     user = UserModel.objects.filter(id=request.data.get("touserid"))
     for data in user:
        serializeConvo =SerializeConversation(data={
            "userid":request.data.get("touserid"),
            "fromuserid": request.data.get("fromuserid"),
            "photo": data.profile_url,
            "name": data.username,
            "message": [request.data.get("usermessage")],
            "date_send": request.data.get("date_send")
        })
        chat = Conversation.objects.filter(userid =request.data.get("touserid"))
        if chat.exists():
           return Response("Already Exists")
        elif not chat.exists():
         if serializeConvo.is_valid():
              serializeConvo.save()
         return Response(serializeConvo.data, status=status.HTTP_200_OK)


class DeleteChatConvo(APIView):
    def post(self, request,id):
       convo =Conversation.objects.filter(id=id)
       ChatModel.objects.all().delete()
       convo.delete()
       return Response({'message': 'Convo Delete Success'}, status=status.HTTP_204_NO_CONTENT)


class DeleteChat(APIView):
    def post(self, request, id):
        chat = ChatModel.objects.filter(id=id)
        chat.delete()
        return Response({'message': 'Chat deleted successfully'}, status=status.HTTP_204_NO_CONTENT)






class ChatConversation(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Get data from request
        from_user_id = request.data.get("fromuserid")
        to_user_id = request.data.get("touserid")
        user_message = request.data.get("usermessage")
        date_send = request.data.get("date_send")
        
        # Validate required fields
        if not all([from_user_id, to_user_id, user_message]):
            return Response(
                {"error": "fromuserid, touserid, and usermessage are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Check if conversation already exists
        existing_chat = Conversation.objects.filter(
            Q(fromuserid=from_user_id, userid=to_user_id) |
            Q(fromuserid=to_user_id, userid=from_user_id)
        ).exists()
        
        if existing_chat:
            return Response(
                {"message": "Chat already exists"},
                status=status.HTTP_200_OK
            )
        

        from_user = UserModel.objects.filter(id=from_user_id).first()
        to_user = UserModel.objects.filter(id=to_user_id).first()
        # Prepare serializers with correct object attributes
        serialize_to_user = SerializeConversation(data={
            "fromuserid": from_user_id,
            "userid": to_user_id,
            "photo": to_user.profile_url[:150] if to_user.profile_url else "",
            "name": to_user.username[:150] if to_user.username else "",
            "message": [user_message],
            "date_send": date_send
        })
        
        serialize_from_user = SerializeConversation(data={
            "fromuserid": to_user_id,
            "userid": from_user_id,
            "photo": from_user.profile_url[:150] if from_user.profile_url else "",
            "name": from_user.username[:150] if from_user.username else "",
            "message": [user_message],
            "date_send": date_send
        })

        
        
        # Validate both serializers
        is_to_valid = serialize_to_user.is_valid()
        is_from_valid = serialize_from_user.is_valid()
        
        if is_to_valid and is_from_valid:
            serialize_to_user.save()
            serialize_from_user.save()
            
            return Response({
                "Chat": {
                    "User": serialize_from_user.data,
                    "ChatMate": serialize_to_user.data
                }
            }, status=status.HTTP_201_CREATED)
        
        # Return validation errors
        return Response({
            "errors": {
                "from_user": serialize_from_user.errors if not is_from_valid else {},
                "to_user": serialize_to_user.errors if not is_to_valid else {}
            }
        }, status=status.HTTP_400_BAD_REQUEST)

class getConversation(APIView):
      permission_classes = [IsAuthenticated]
      def get(self,req, pk):    
       convo =Conversation.objects.filter(fromuserid =pk)
       for data in convo:
          chat =ChatModel.objects.filter(fromuserid=data.fromuserid)
          for chats in chat:
            user = UserModel.objects.filter(id=data.userid)
            for users in user:
              data.photo = users.profile_url
              data.name = users.username
              data.message.append(chats.usermessage)
       chatserial =SerializeConversation(convo, many=True)
       return Response(chatserial.data, status=status.HTTP_200_OK)


# class ChatConversation(APIView):
#   def post(self, request):
#     fromuserid = UserModel.objects.filter(id=request.data.get("touserid"))
#     for data in fromuserid:
#          serializetouserid =SerializeConversation(data={
#             "fromuserid":request.data.get("fromuserid"),
#             "userid": request.data.get("touserid"),
#             "photo": data.profile_url,
#             "name": data.username,
#             "message": [request.data.get("usermessage")],
#             "date_send": request.data.get("date_send")
#         })
#     touserid =UserModel.objects.filter(id =request.data.get("fromuserid"))
#     for datum in touserid:
#         serializefromuserid =SerializeConversation(data={
#             "fromuserid": request.data.get("touserid"),
#             "userid":request.data.get("fromuserid"),
#             "photo": datum.profile_url,
#             "name": datum.username,
#             "message": [request.data.get("usermessage")],
#             "date_send": request.data.get("date_send")
#         })
#     existing_chat = Conversation.objects.filter(Q(fromuserid=request.data.get("fromuserid"), userid=request.data.get("touserid")) | Q(fromuserid=request.data.get("touserid"), userid=request.data.get("fromuserid"))).exists()
#     if existing_chat:
#         return Response("Already Exists")
#     else:
#         if serializefromuserid.is_valid() and serializetouserid.is_valid():
#            serializefromuserid.save()
#            serializetouserid.save() 
#     return Response({"Chat":{"User":serializefromuserid.data,"ChatMate":serializetouserid.data}}, status=status.HTTP_200_OK)
    


class Chat(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self, request):

     serializeChatfromuser = SerializeChat(data={
    "fromuserid": request.data.get("fromuserid"),
    "touserid": request.data.get("touserid"),
    "usermessage": request.data.get("usermessage"),
    "isUser": True,
    "date_send": request.data.get("date_send")
     })

     serializeChatTouser = SerializeChat(data={
    "fromuserid": request.data.get("touserid"),
    "touserid": request.data.get("fromuserid"),
    "usermessage": request.data.get("usermessage"),
    "isUser": False,
    "date_send": request.data.get("date_send")
     })


     if serializeChatfromuser.is_valid() and serializeChatTouser.is_valid():
      serializeChatfromuser.save()
      serializeChatTouser.save()

      return Response({
                "Chat": {
                    "User": serializeChatfromuser.data,
                    "ChatMate": serializeChatTouser.data
                }
            }, status=status.HTTP_200_OK)
     else:
        return Response({
        "fromuser_errors": serializeChatfromuser.errors,
        "touser_errors": serializeChatTouser.errors
        }, status=status.HTTP_400_BAD_REQUEST)

   
    
class getUserChat(APIView):
   permission_classes = [IsAuthenticated]
   def get(self, req, fromuserid, touserid):
      user =ChatModel.objects.filter(Q(fromuserid=fromuserid, touserid=touserid))
      chat =SerializeChat(user, many=True)
      return Response(chat.data,status=status.HTTP_200_OK)
     

class getToUserChat(APIView):
   permission_classes = [IsAuthenticated]
   def get(self, req, touserid):
     user =ChatModel.objects.filter(touserid=touserid)
     chat =SerializeChat(user, many=True)
     return Response(chat.data,status=status.HTTP_200_OK)

class searchUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, req, email):
     user = UserModel.objects.filter(email=email)
     serializer = SerializeUser(user, many=True)
     return Response(serializer.data, status=status.HTTP_200_OK)
    

class updateUser(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, userid):
      # name = request.data.get('name')
      # name = request.data.get('name')
      # user =UserModel.objects.filter(id=userid)
      # for user in user:
     try:
        user = UserModel.objects.get(id=userid)
     except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
     serializer = SerializeUser(user, data=request.data, partial=True)
     if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         

  
    



class TimeClockViewUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, userID):
     clockin = TimeInOutClock.objects.filter(userID=userID)
     if clockin is None:
        return JsonResponse({"error": "No Data"}, status=404)
     elif clockin is not None:
        serializer = SerializeClockInOut(clockin, many=True)
     return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def registerwithGoogle(request):
    email = request.data.get('email')
    username = request.data.get('username')
    photo_url = request.data.get('photo_url')
    try:
        if UserModel.objects.filter(email=email).exists():
          user = UserModel.objects.get(email=email)
          tokens = get_tokens_for_user(user)
          return Response({
                "user": Serializelogin(user).data,
                "tokens": tokens,
            }, status=status.HTTP_200_OK)
        else: 
         user = UserModel.objects.create_user(username=username, email=email, date_joined=date.today(), profile_url=photo_url)
         user.is_active = True
         user.save()
         tokens = get_tokens_for_user(user)
        return Response({
            "user": Serializelogin(user).data,
            "tokens": tokens,
        }, status=status.HTTP_201_CREATED)
    except UserModel.DoesNotExist:
        return Response({"error": "User not Found"}, status=status.HTTP_401_UNAUTHORIZED)

  
@api_view(['POST'])
def registerwithFacebook(request):
  email = request.data.get('email')
  username = request.data.get('username')
  photo_url = request.data.get('photo_url')
  try:
       if UserModel.objects.filter(email=email).exists():
          user = UserModel.objects.get(email=email)
          tokens = get_tokens_for_user(user)
          return Response({
                "user": Serializelogin(user).data,
                "tokens": tokens,
            }, status=status.HTTP_200_OK)
       else: 
         user = UserModel.objects.create_user(username=username, email=email, date_joined=date.today(), profile_url=photo_url )
         user.is_active = True
         user.save()
         tokens = get_tokens_for_user(user)
         return Response({
            "user": Serializelogin(user).data,
            "tokens": tokens,
        }, status=status.HTTP_201_CREATED)
  except UserModel.DoesNotExist:
        return Response({"error": "User not Found"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def register(request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if UserModel.objects.filter(email=email).exists():
         return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = UserModel.objects.create_user(username=username, email=email, password=password, date_joined=date.today(), )
        user.is_active = True
        user.save()
        tokens = get_tokens_for_user(user)
        return Response({
            "user": Serializelogin(user).data,
            "tokens": tokens,
        }, status=status.HTTP_201_CREATED)

def home(request):
    return HttpResponse("Welcome to Timelock API")
    



