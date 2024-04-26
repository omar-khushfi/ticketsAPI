from rest_framework import serializers
from tickets.models import *
from .models import *


class Movieserializer(serializers.ModelSerializer):
    class Meta :
        model=Movie
        fields='__all__'
        
class Reservationserializer(serializers.ModelSerializer):
    class Meta :
        model=Reservation
        fields='__all__'


class Guestserializer(serializers.ModelSerializer):
    class Meta:
        model=Guest
        fields=['pk','reservation','name','mobile']

class Postserializer(serializers.ModelSerializer):
     class Meta :
        model=Reservation
        fields='__all__'