from rest_framework import serializers
from apps.WH_auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'telephone', 'username', 'email', 'is_staff', 'is_active')


