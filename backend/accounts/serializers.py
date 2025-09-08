from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login

class ProfileSerializer(serializers.ModelSerializer):
    # 읽기 전용 필드 (계산된 속성)
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Profile
        fields = ['gender', 'birth_date', 'age', 'bio', 'phone_number', 'profile_picture']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'date_joined','last_login')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user

class UserMeSerializer(serializers.ModelSerializer):
    """
    /me 전용 Serializer (User + Profile 조회 및 수정)
    - 읽기: 유저 + 프로필 중첩 반환
    - 쓰기(PATCH): first_name/last_name/email/password + profile.* 동시 부분 수정
    """
    profile = ProfileSerializer(required=False)
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = (
            "id", "username", "first_name", "last_name", "email",
            "date_joined", "last_login", "password", "profile"
        )
        read_only_fields = ("id", "username", "date_joined", "last_login")

    def update(self, instance, validated_data):
        # 비밀번호는 별도 처리
        password = validated_data.pop("password", None)
        profile_data = validated_data.pop("profile", None)

        # User 기본 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 비밀번호 변경
        if password:
            instance.set_password(password)
            instance.save()

        # Profile 업데이트(없으면 생성)
        if profile_data is not None:
            profile, _ = Profile.objects.get_or_create(user=instance)
            # Nested update: 부분 업데이트 허용
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance
    
    
# 토큰 발급 시 마지막 로그인 시간 업데이트 하도록 오버라이드
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # 로그인 성공하면 self.user가 여기에 존재
        update_last_login(None, self.user)
        return data