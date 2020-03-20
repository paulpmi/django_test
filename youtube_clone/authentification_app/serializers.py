from rest_framework import serializers

from youtube_clone.authentification_app.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            name=validated_data['name']
        )
        user.encode_password(validated_data['password'])
        user.save()
        return str(user.activation_token)
