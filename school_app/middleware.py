"""
Middleware for St. Xavier's School website.

Tracks every page load by incrementing today's visit counter.
Every request (including refreshes and repeat visits) counts as a visit.
"""

from datetime import date
from django.db.models import F
from .models import DailyVisitCount


class VisitCounterMiddleware:
    """
    Middleware that increments the daily visit counter on every page request.

    - Static files and admin pages are excluded to avoid inflating counts
    - Uses get_or_create + F() expression for atomic, race-condition-safe increments
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only count actual page views, not static/media/admin requests
        path = request.path
        if not path.startswith('/static/') and \
           not path.startswith('/media/') and \
           not path.startswith('/admin/') and \
           not path.startswith('/favicon'):

            today = date.today()
            # Atomic increment: creates row if it doesn't exist, then increments
            obj, created = DailyVisitCount.objects.get_or_create(
                date=today,
                defaults={'count': 1}
            )
            if not created:
                # Use F() expression for thread-safe increment
                DailyVisitCount.objects.filter(date=today).update(count=F('count') + 1)

        response = self.get_response(request)
        return response
