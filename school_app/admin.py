"""
Django Admin configuration for St. Xavier's School website.

This module customizes the Django admin panel to provide a user-friendly
interface for managing school notices. Administrators can:
- Add new notices with PDF attachments
- Edit existing notices
- Toggle notice visibility (active/inactive)
- Search and filter notices by date

NO CODE CHANGES are required to manage notices - everything is done
through the admin panel at /admin/
"""

from django.contrib import admin
from .models import Notice, DailyVisitCount


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Notice model.

    Features:
    - List view shows title, date, and active status at a glance
    - Inline editing of the active status (toggle visibility without opening)
    - Filter by active status and publication date
    - Search by title and description
    - Date-based navigation hierarchy
    """

    # =========================================================================
    # LIST VIEW CONFIGURATION
    # =========================================================================

    # Columns displayed in the notice list
    list_display = ('title', 'published_date', 'is_active')

    # Allow toggling is_active directly from the list view
    list_editable = ('is_active',)

    # Filter sidebar options
    list_filter = ('is_active', 'published_date')

    # Search functionality - search by title or description
    search_fields = ('title', 'description')

    # Date-based drill-down navigation
    date_hierarchy = 'published_date'

    # Number of notices per page in admin
    list_per_page = 20

    # =========================================================================
    # FORM CONFIGURATION
    # =========================================================================

    # Fields shown when adding/editing a notice
    fields = ('title', 'description', 'pdf_file', 'is_active')

    # Read-only fields (published_date is auto-set)
    readonly_fields = ('published_date',)


# =============================================================================
# ADMIN SITE CUSTOMIZATION
# =============================================================================
# Customize the admin panel header and title
admin.site.site_header = "St. Xavier's School - Administration"
admin.site.site_title = "St. Xavier's School Admin"
admin.site.index_title = "School Website Management"


@admin.register(DailyVisitCount)
class DailyVisitCountAdmin(admin.ModelAdmin):
    """Admin view for website visit statistics (read-only)."""
    list_display = ('date', 'count')
    list_filter = ('date',)
    date_hierarchy = 'date'
    ordering = ['-date']

    def has_add_permission(self, request):
        return False  # Visits are tracked automatically

    def has_change_permission(self, request, obj=None):
        return False  # Prevent manual edits

