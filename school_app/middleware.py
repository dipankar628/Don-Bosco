# school_app/middleware.py
from django.db import OperationalError
# ... keep your existing imports ...

class VisitCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ... your existing logic for fetching 'today' date ...

        try:
            # Try updating the visitor counter table normally
            DailyVisitCount.objects.filter(date=today).update(count=F('count') + 1)
        except OperationalError as e:
            # If deploying on Vercel read-only system, fail silently so the page loads anyway!
            if "readonly database" in str(e):
                pass
            else:
                raise e

        response = self.get_response(request)
        return response
