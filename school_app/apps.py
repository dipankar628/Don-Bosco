"""
App configuration for the School App.

This is the primary Django application for the St. Xavier's School website.
It handles all pages, the Notice model, and admin panel customization.
"""

from django.apps import AppConfig


class SchoolAppConfig(AppConfig):
    """Configuration class for the school_app application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school_app'
    verbose_name = "St. Xavier's School Website"
