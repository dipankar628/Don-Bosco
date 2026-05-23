import datetime
from django.db.models import F
from django.db import OperationalError

# We wrap the import in a try/except or pull it directly to ensure Django finds it
try:
    from school_app.models import DailyVisitCount
except ImportError:
    from .models import DailyVisitCount

class VisitCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip asset paths so we don't track image or CSS hits
        if not request.path.startswith('/static/') and not request.path.startswith('/media/'):
            today = datetime.date.today()
            
            try:
                # Safely attempt to increment the visitor counter
                DailyVisitCount.objects.filter(date=today).update(count=F('count') + 1)
            except (OperationalError, NameError) as e:
                # If Vercel blocks it (read-only) or the model class isn't matching, bypass gracefully
                pass

        response = self.get_response(request)
        return response
