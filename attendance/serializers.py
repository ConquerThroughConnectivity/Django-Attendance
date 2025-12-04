from datetime import datetime
from rest_framework import serializers  
from django.contrib.auth import authenticate

from attendance.models import AttendanceRecordsModels, ChatModel, Conversation, LoginModel, TimeInOutClock, UserModel






class SerializeUser(serializers.ModelSerializer):
    # userID = serializers.IntegerField(source='id') 
    class Meta:
        model = UserModel
        fields  = '__all__'
class Serializelogin(serializers.ModelSerializer):
    class Meta:
        model = LoginModel
        fields =['id', 'email', 'password', 'username']
class SerializeClockInOut(serializers.ModelSerializer):
    class Meta:
        model = TimeInOutClock
        fields =['id', 'userID', 'time_in', 'time_out', 'time_in_description', 'time_out_description','time_out_location','time_in_location' ,'date', 'hrs']

class SerializeChat(serializers.ModelSerializer):
    class Meta:
        model =ChatModel
        fields =['id', 'fromuserid','touserid','usermessage', 'isUser','date_send']

class SerializeRecords(serializers.ModelSerializer):
    class Meta:
       model = AttendanceRecordsModels
       fields ='__all__'

class SerializeConversation(serializers.ModelSerializer):
    class Meta:
        model =Conversation
        fields =['id','fromuserid','userid','photo','name','message','date_send']

class LoginSerialize(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
       user = authenticate(**data)
       if user and user.is_active:
            return user
       raise serializers.ValidationError("Incorrect credentials!")
  
