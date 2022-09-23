from rest_framework import serializers


class LikeAnalyticsOutputSerializer(serializers.Serializer):
    date = serializers.DateField()
    likes = serializers.IntegerField()
