from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class StaffOnlyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, values):
        data = super().validate(values)

        if not self.user.is_staff:
            raise serializers.ValidationError(_("Only staff members are allowed to obtain a token."))

        return data