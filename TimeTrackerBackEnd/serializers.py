from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import ProjectModel, TaskModel, FrameModel


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'})

        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "last_login", "username",
                  "first_name", "last_name", "email"]

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'})

        user.set_password(password)
        user.save()
        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    # The default value of the project returns all projects, but should return only user projects or nothing.
    # project = serializers.PrimaryKeyRelatedField(queryset=ProjectModel.objects.filter(user=None))
    class Meta:
        model = TaskModel
        fields = '__all__'


class FrameSerializer(serializers.ModelSerializer):
    # todo: validate start and stop. Start must be less stop
    class Meta:
        model = FrameModel
        fields = '__all__'
