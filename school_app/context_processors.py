"""
Context processors for St. Xavier's School website.

Makes visit counter data available to ALL templates automatically,
so the counter can be displayed in the footer or any page.
"""

from datetime import date
from django.db.models import Sum
from .models import DailyVisitCount


def visit_counts(request):
    """
    Adds today's visit count and total lifetime visits to every template context.

    Template variables:
        {{ today_visits }}  — Number of page loads today
        {{ total_visits }}  — Lifetime total page loads across all days
    """
    today = date.today()

    # Get today's count
    try:
        today_obj = DailyVisitCount.objects.get(date=today)
        today_count = today_obj.count
    except DailyVisitCount.DoesNotExist:
        today_count = 0

    # Get lifetime total (sum of all daily counts)
    total = DailyVisitCount.objects.aggregate(total=Sum('count'))['total'] or 0

    return {
        'today_visits': today_count,
        'total_visits': total,
    }
