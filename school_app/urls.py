"""
URL patterns for St. Xavier's School, Harmutty website.

Maps URL paths to their corresponding view functions.
All URLs use named patterns for easy reverse lookups in templates
(e.g., {% url 'home' %}, {% url 'academics' %}).
"""

from django.urls import path
from . import views

# =============================================================================
# APP URL PATTERNS
# =============================================================================
urlpatterns = [
    # Homepage - displays carousel, principal's desk, stats, notices, gallery
    path('', views.home, name='home'),

    # Academics page - CBSE info, streams, curriculum, co-curriculars
    path('academics/', views.academics, name='academics'),

    # Campus page - facilities, gallery
    path('campus/', views.campus, name='campus'),

    # Faculty page - teacher profiles grid
    path('faculty/', views.faculty, name='faculty'),

    # Contact page - contact info, form, map
    path('contact/', views.contact, name='contact'),

    # Notices page - all active notices with PDF downloads
    path('notices/', views.notices_list, name='notices'),
]
