# django-jwt-account-template

Django + MySQL 기반의 계정(회원가입/로그인/로그아웃/프로필) 백엔드 템플릿입니다.  
JWT 인증(DRF SimpleJWT)과 Docker Compose를 기본 제공하며, 프런트엔드는 포함하지 않습니다.

- **Stack**: Django, Django REST Framework, SimpleJWT, MySQL 8, Docker Compose
- **Use case**: 회원가입/인증/프로필을 빠르게 붙일 수 있는 백엔드 스타터

## 📦 Docker Hub
이미지: [<your-dockerhub-username>/django-jwt-account](<PUT-YOUR-DOCKER-HUB-LINK-HERE>)


## ▶️ 빠른 시작

# 빌드 및 실행
docker compose up -d --build

API 기본 포트: http://localhost:8002

## 🔐 인증/계정 API (예시)

- 회원가입: POST /api/accounts/register/

- 로그인(JWT 발급): POST /api/token/

- 토큰 갱신: POST /api/token/refresh/

- 내 프로필 조회/수정: GET|PATCH /api/accounts/me/ (Authorization: Bearer <access>)

## 🧰 개발 메모

- .env는 커밋 금지, 대신 .env.example로 키 목록만 제공

- Docker Hub 이미지는 위 링크 참고

## 📝 라이선스

- MIT (필요 시 변경)