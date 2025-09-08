from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)
from .views import RegisterView, MeView, CustomTokenObtainPairView, LogoutView



# https://jwt.io/를 통해 jwt의 내용을 해석가능

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("me/", MeView.as_view(), name="me"),  # Uer + Profile 조회/수정
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('logout/', LogoutView.as_view(), name='logout'),            # 단일 기기 로그아웃
]
