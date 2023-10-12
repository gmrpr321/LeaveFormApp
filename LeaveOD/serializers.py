from rest_framework import serializers
from .models import User, Form


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = "__all__"


class ExcelUploadSerializer(serializers.Serializer):
    excel_file = serializers.FileField()