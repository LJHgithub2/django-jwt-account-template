from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer

from .serializers import (
    UserRegisterSerializer,
    UserMeSerializer,
)
from .models import Profile

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer의 save()메소드를 호출하면 내부 함수인 create() 메서드가 작동한다.
        user = serializer.save()
        # 프로필 자동 생성 보장(혹시 시그널 누락시 대비)
        Profile.objects.get_or_create(user=user)
        return Response(
            {"user": UserRegisterSerializer(user, context=self.get_serializer_context()).data,
             "message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )
    
# RetrieveUpdateAPIView: GET, PUT, PATCH 메서드 지원
class MeView(generics.RetrieveUpdateAPIView):
    """
    GET /me   : 내 정보 + 프로필 조회
    PATCH /me : 내 정보 + 프로필 부분 수정(멀티파트 지원: profile_picture 업로드)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserMeSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    # 인증된 사용자 자신의 User 객체를 반환
    def get_object(self):
        # select_related로 user 모델과 프로필 모델을 조인해 한번에 리스트 가져옴
        user_qs = User.objects.select_related("profile")
        try:
            user = user_qs.get(pk=self.request.user.pk)
        except User.DoesNotExist:
            # 이 케이스는 사실상 발생하지 않지만 방어적으로 처리
            raise
        return user
    
# 토큰 발급 시 마지막 로그인 시간 업데이트 하도록 오버라이드
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # body 또는 쿠키에서 refresh 추출
        refresh_token = request.data.get("refresh") or request.COOKIES.get("refresh")
        if not refresh_token:
            return Response({"detail": "refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # ✅ 이제 이 refresh는 재사용 불가
        except TokenError:
            # 이미 블랙리스트이거나 불량 토큰인 경우
            return Response({"detail": "invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        # 클라이언트는 access/refresh를 로컬에서 제거 필수
        return Response(status=status.HTTP_205_RESET_CONTENT)