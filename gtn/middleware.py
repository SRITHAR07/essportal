from django.utils.timezone import now
from django.contrib.sessions.models import Session
from ess.models import GennhrAudit,Users  
from ess.views import get_client_ip  # Import the function to get the client's IP
from django.utils import timezone
class SessionExpiryLoggerMiddleware:
    """Middleware to log session expiration events in GennhrAudit."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.log_expired_sessions(request)
        return response

    def log_expired_sessions(self, request):
        """Log session expiration for users whose sessions have expired."""
        expired_sessions = Session.objects.filter(expire_date__lt=now())

        for session in expired_sessions:
            session_data = session.get_decoded()
            empid = session_data.get("empid")

            if empid:
                # Fetch the actual user ID from the Users table
                try:
                    user = Users.objects.get(empid=empid)
                    user_id = user.pk  # Get the primary key
                except Users.DoesNotExist:
                    user_id = None  # Fallback if user not found

                # ✅ Log session expiration with the correct user ID
                GennhrAudit.objects.create(
                    datetime=timezone.now(),
                    ip=get_client_ip(request),
                    user=user_id,  # Store actual user ID instead of empid
                    table="Users",
                    action="Session Expired",
                    description=f"User session expired due to inactivity. (EmpID: {empid})"
                )

            session.delete()  # Delete expired session
