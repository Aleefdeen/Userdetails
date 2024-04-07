from rest_framework.serializers import ModelSerializer
from userdetails.models import UserDetails


class UserDetailsSerializer(ModelSerializer):
    
    class Meta:
        model = UserDetails
        fields = "__all__"


class LoginUserDetailsSerializer(ModelSerializer):
    
    class Meta:
        model = UserDetails
        fields = ["email", "password"]