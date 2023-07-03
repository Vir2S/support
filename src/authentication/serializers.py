from rest_framework import serializers


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
