from rest_framework.serializers import ModelSerializer
from product_inventory.models import Products,User
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from rest_framework import serializers
from django.utils.translation import gettext as _

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email', 'password']
        extra_kwargs = {'password':{'write_only':True, 'min_length':5}}

    def create(self,validated_data):
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg,code='authorizarion')
        attrs['user'] = user
        return attrs

