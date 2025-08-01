from .models import Visit
from django.utils.deprecation import MiddlewareMixin

def get_client_ip(request):
    """Get client IP address, accounting for proxies."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")

class TrackIPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Ensure session exists
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        ip = get_client_ip(request)

        # Log only if we haven't seen this session before
        if not Visit.objects.filter(session_key=session_key).exists():
            Visit.objects.create(ip_address=ip, session_key=session_key)
