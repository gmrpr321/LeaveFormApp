from rest_framework import serializers
from .models import User, Form


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = "__all__"


class FormSerializer(serializers.Serializer):
    class Meta:
        model = Form
        fields = "__all__"
