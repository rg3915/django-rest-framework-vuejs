from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        )
