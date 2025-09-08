# 공통 유틸: get_client_ip, 신뢰 프록시 판별 등
import os
from ipaddress import ip_address, ip_network

def parse_networks(raw: str):
    nets = []
    for s in [x.strip() for x in raw.split(",") if x.strip()]:
        nets.append(ip_network(s, strict=False))
    return nets

def remote_is_trusted(remote: str, trusted_networks):
    try:
        rip = ip_address(remote)
    except ValueError:
        return False
    return any(rip in n for n in trusted_networks)

def get_client_ip(request):
    """신뢰 프록시라면 XFF의 첫 IP, 아니면 REMOTE_ADDR"""
    trusted = parse_networks(os.getenv("DJANGO_TRUSTED_PROXIES", ""))
    remote = request.META.get("REMOTE_ADDR", "")
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff and remote_is_trusted(remote, trusted):
        return xff.split(",")[0].strip()
    return remote
