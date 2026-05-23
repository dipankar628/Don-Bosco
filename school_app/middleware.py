import datetime
from django.db.models import F
from django.db import OperationalError
from .models import DailyVisitCount

class VisitCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only count standard page views, ignore asset requests like images/CSS
        if not request.path.startswith('/static/') and not request.path.startswith('/media/'):
            today = datetime.date.today()
            
            try:
                # 1. Try to fetch or initialize the record for today
                obj, created = DailyVisitCount.objects.get_or_create(date=today)
                
                # 2. Increment the count safely
                DailyVisitCount.objects.filter(date=today).update(count=F('count') + 1)
            except OperationalError as e:
                # If on Vercel's read-only file system, bypass the crash so the site loads
                if "readonly database" in str(e):
                    pass
                else:
                    raise e

        response = self.get_response(request)
        return response
