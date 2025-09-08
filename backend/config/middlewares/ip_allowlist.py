# config/middlewares/ip_allowlist.py
import os
import logging
from ipaddress import ip_address, ip_network
from django.http import HttpResponseForbidden, JsonResponse
from .net import parse_networks, get_client_ip

logger = logging.getLogger("ip_allowlist")

class IPAllowlistMiddleware:
    """
    DJANGO_ALLOWED_IPS=common.env 에 설정
    DJANGO_TRUSTED_PROXIES=common.env 에 설정
    DJANGO_SHOW_FORBIDDEN_IP=common.env 에 설정
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.networks = parse_networks(os.getenv("DJANGO_ALLOWED_IPS", ""))
        # 로컬 루프백 기본 허용(원치 않으면 제거)
        if "127.0.0.1" not in os.getenv("DJANGO_ALLOWED_IPS", ""):
            self.networks += [ip_network("127.0.0.1"), ip_network("::1")]
        self.show_ip_in_response = os.getenv("DJANGO_SHOW_FORBIDDEN_IP", "false").lower() == "true"

    def __call__(self, request):
        client_ip = get_client_ip(request)
        # IP 파싱 검증
        try:
            ip_obj = ip_address(client_ip)
        except ValueError:
            logger.warning("IP blocked (invalid): ip=%s path=%s", client_ip, request.path)
            return self._forbid(client_ip)

        # 허용 목록 검사 (허용 목록이 비어 있으면 모두 허용. 기본 차단 원하면 조건 바꿔도 됨)
        if self.networks and not any(ip_obj in net for net in self.networks):
            logger.warning("IP blocked: ip=%s path=%s", client_ip, request.path)
            return self._forbid(client_ip)

        return self.get_response(request)

    def _forbid(self, client_ip: str):
        if self.show_ip_in_response:
            return JsonResponse({"detail": "Forbidden", "ip": client_ip}, status=403)
        return HttpResponseForbidden("Forbidden")
