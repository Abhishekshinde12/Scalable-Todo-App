from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type' : 'password'})

    class Meta:
        model = MyUser
        # subset of fields to be used in the model serializer
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']
        # as the password field already present in model - hence setting it as write only that is not include in the response, only accept it in the request
        extra_kwargs = {
            'password' : {'write_only' : True, 'style' : {'input_type' : 'password'}}
        }

    def validate(self, attrs):
        # check if passwords match
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs
    
    def create(self, validated_data):
        # remove password2 as it's not a model field
        validated_data.pop('password2')
        # removing password, as not stored directly in the DB
        password = validated_data.pop('password')

        # create user instance
        user = MyUser(**validated_data)
        user.set_password(password) # hash password
        user.save()
        return user




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # USERNAME field of the model
    # which would be used for unique identification in the request body
    username_field = 'email'

    # even after setting email as username field, serializer doesn't auto create DRF field called email for validation
    # adding this ensures - field available in the serializer input, properly validate email, also work correctly in DRF API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField()

    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = MyUser.objects.get(email=attrs['email'])
        user_data = {
            'refresh' : data['refresh'],
            'access' : data['access'],
            'user' : {
                'user_id' : user.id,
                'username' : f'{user.first_name} {user.last_name}'
            }
        }
        return user_data