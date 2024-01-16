from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'],
            generation=validated_data['generation'],
            role=validated_data['role'],
            workout_location=validated_data['workout_location'],
            workout_level=validated_data['workout_level'],
            profile_number=validated_data['profile_number'],
        )
        return user

    def validate(self, data):
        required_fields = [
            'email',
            'password',
            'username',
            'generation',
            'role',
            'workout_location',
            'workout_level',
            'profile_number',
        ]

        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError(f"{field} 필드는 비어 있을 수 없습니다.")

        return data

