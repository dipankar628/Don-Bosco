"""
URL configuration for St. Xavier's School, Harmutty website.

Routes:
    /admin/     - Django admin panel (for managing notices)
    /           - School website pages (handled by school_app)
    /media/...  - Uploaded media files (notice PDFs) served in development
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# =============================================================================
# PROJECT URL PATTERNS
# =============================================================================
urlpatterns = [
    # Django Admin Panel - Accessible at /admin/
    # Used by administrators to add/edit/delete notices with PDF attachments
    path('admin/', admin.site.urls),

    # School Website - All pages handled by school_app
    # Includes: home, academics, campus, faculty, contact, notices
    path('', include('school_app.urls')),
]

# =============================================================================
# MEDIA FILE SERVING (Development Only)
# =============================================================================
# In development, Django serves uploaded media files (notice PDFs)
# In production, configure your web server (Nginx/Apache) to serve these
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
