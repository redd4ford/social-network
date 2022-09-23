from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserActivityStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'last_login',
            'last_request_time',
        ]
