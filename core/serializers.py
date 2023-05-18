from rest_framework import serializers
from . models import User, Campaign


class SubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)