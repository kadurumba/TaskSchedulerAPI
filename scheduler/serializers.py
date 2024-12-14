from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task
from django.utils import timezone
import re


class RegisterSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=150)
    # email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True,  min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}, 'email': {'required': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_password(self, value):
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter and one digit.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(username=validated_data['username'],
                                            password=validated_data['password']
                                            )
            return user


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_completed = serializers.SerializerMethodField()
    is_pending = serializers.SerializerMethodField()
    scheduled_time = serializers.DateTimeField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'scheduled_time', 'created_at', 'updated_at', 'status', 'is_completed', 'is_pending', 'user']
        read_only_fields = ['created_at', 'updated_at', 'status', 'is_completed', 'is_pending']

    def is_completed(self, obj):
        return obj.scheduled_time <= timezone.now() and obj.status == 'completed'

    def is_pending(self, obj):
        return obj.status == 'pending' and obj.scheduled_time > timezone.now()

    def create(self, validated_data):
            request = self.context.get('request')
            validated_data['user'] = request.user  # Ensure user is set from the request
            return super().create(validated_data)
