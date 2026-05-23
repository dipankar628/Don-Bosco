"""
Models for St. Xavier's School, Harmutty website.

This module defines models for Notices, Daily Website Tracking, and Faculty management
which allows administrators to handle content entirely through the Django admin panel.
"""

from django.db import models


class Notice(models.Model):
    """
    Model representing a school notice or circular.

    Administrators can manage notices entirely through the Django admin panel:
    - Add new notices with a title, optional description, and PDF attachment
    - Toggle notice visibility using the is_active field
    - Notices are automatically ordered by date (newest first)

    Fields:
        title (str): The title of the notice (max 200 characters)
        description (str): Optional brief description of the notice
        pdf_file (File): The PDF file attachment uploaded via admin
        published_date (date): Auto-set to the date the notice was created
        is_active (bool): Controls whether the notice is visible on the website
    """

    # Title of the notice - displayed on the website
    title = models.CharField(
        max_length=200,
        help_text="Enter the title of the notice (e.g., 'Exam Schedule 2025')"
    )

    # Optional description - shown below the title on the website
    description = models.TextField(
        blank=True,
        help_text="Optional: Add a brief description of the notice"
    )

    # PDF file upload - stored in media/notices/ directory
    pdf_file = models.FileField(
        upload_to='notices/',
        help_text="Upload the notice PDF file"
    )

    # Auto-set publication date
    published_date = models.DateField(
        auto_now_add=True,
        help_text="Automatically set when the notice is created"
    )

    # Toggle visibility without deleting
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this notice from the website"
    )

    class Meta:
        ordering = ['-published_date']  # Newest notices appear first
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'

    def __str__(self):
        """Return the notice title for display in admin panel."""
        return self.title


class FacultyMember(models.Model):
    """
    Model representing a teacher or staff member at St. Xavier's School.

    Administrators can manage staff entries entirely through the Django admin panel:
    - Add or remove teachers with their name, photo, and assigned subjects
    - Assign structural designations (e.g., Principal, Teacher)
    - Order positions manually using a custom numeric sort key

    Fields:
        name (str): Full name of the faculty member
        designation (str): Structural tier choice (Principal, Staff, etc.)
        subject_or_role (str): Main subjects taught or office department role
        photo (Image): Portrait photo upload field (optional)
        sort_order (int): Numeric weight to prioritize who sits at the top of the webpage
        is_active (bool): Controls visibility on the public faculty page
    """

    # Category choices mapping official tiers
    DESIGNATION_CHOICES = [
        ('ADMIN_PR', 'Principal'),
        ('ADMIN_VP', 'Vice Principal'),
        ('TEACHER', 'Teaching Staff'),
        ('OFFICE', 'Non-Teaching / Support Staff'),
    ]

    # Full display name
    name = models.CharField(
        max_length=150,
        help_text="Enter full name (e.g., 'Fr. Joshua' or 'Mr. Dipankar Holder')"
    )

    # Core administrative tier selection
    designation = models.CharField(
        max_length=40,
        choices=DESIGNATION_CHOICES,
        default='TEACHER',
        help_text="Select their official rank layout category"
    )

    # Subjects or desk designation details
    subject_or_role = models.CharField(
        max_length=150,
        help_text="Enter role or subjects (e.g., 'Computer Science & Vocational Education')"
    )

    # Optional staff portrait photo
    photo = models.ImageField(
        upload_to='faculty_photos/',
        blank=True,
        null=True,
        help_text="Optional: Upload a square portrait photo"
    )

    # Controls webpage presentation ranking (e.g. Principal=1, Vice Principal=2, etc.)
    sort_order = models.PositiveIntegerField(
        default=10,
        help_text="Lower values appear first on the webpage layout (e.g., set Principal to 1)"
    )

    # Quick toggle status switch
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck this instead of deleting if the staff member is temporarily on leave"
    )

    class Meta:
        ordering = ['sort_order', 'name']  # Sorted by structural rank weight, then alphabetically
        verbose_name = 'Faculty Member'
        verbose_name_plural = 'Faculty Members'

    def __str__(self):
        return f"{self.name} ({self.get_designation_display()})"


class DailyVisitCount(models.Model):
    """
    Model to track website visits on a per-day basis.
    """

    date = models.DateField(
        unique=True,
        help_text="The date for this visit count"
    )

    count = models.PositiveIntegerField(
        default=0,
        help_text="Total page loads on this date"
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Daily Visit Count'
        verbose_name_plural = 'Daily Visit Counts'

    def __str__(self):
        return f"{self.date}: {self.count} visits"