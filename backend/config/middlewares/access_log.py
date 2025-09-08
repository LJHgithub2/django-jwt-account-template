# config/middlewares/access_log.py
import time
import logging
from .net import get_client_ip

logger = logging.getLogger("access")

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        dur = int((time.perf_counter() - start) * 1000)

        user = getattr(request, "user", None)
        uname = user.username if (user and user.is_authenticated) else "-"

        logger.info(
            'method=%s path="%s" status=%s ms=%s user=%s ip=%s ua="%s"',
            request.method,
            request.get_full_path(),
            response.status_code,
            dur,
            uname,
            get_client_ip(request),
            (request.META.get("HTTP_USER_AGENT", "")[:200]).replace('"', "'"),
        )
        return response
