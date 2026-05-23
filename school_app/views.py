"""
Views for St. Xavier's School, Harmutty website.

Each view renders a specific page of the school website.
The home and notices views pass dynamic data (notices from the database)
to their templates. All other views render static HTML templates that
can be edited directly for content updates.
"""

from django.shortcuts import render
from .models import Notice


def home(request):
    """
    Homepage view - renders the main landing page.

    Displays:
    - Hero carousel with school images
    - Principal's Desk section
    - Quick stats (students, faculty, years, results)
    - Latest 5 active notices from the database
    - Gallery preview

    Context:
        notices: QuerySet of the 5 most recent active notices
    """
    # Fetch the 5 most recent active notices for the homepage
    notices = Notice.objects.filter(is_active=True)[:5]
    return render(request, 'school_app/index.html', {'notices': notices})


def academics(request):
    """
    Academics page view.

    Displays CBSE affiliation details, class structure,
    streams offered, curriculum highlights, and co-curricular activities.
    Content is editable directly in the academics.html template.
    """
    return render(request, 'school_app/academics.html')


def campus(request):
    """
    Campus page view.

    Displays campus overview, facilities grid, and image gallery.
    Content is editable directly in the campus.html template.
    """
    return render(request, 'school_app/campus.html')


def faculty(request):
    """
    Teaching Faculty page view.

    Displays faculty member profiles in a responsive card grid.
    Faculty information is editable directly in the faculty.html template.
    To add/remove faculty, simply edit the HTML file.
    """
    return render(request, 'school_app/faculty.html')


def contact(request):
    """
    Contact page view.

    Displays contact information, a contact form, and Google Maps embed.
    Contact details are editable directly in the contact.html template.
    """
    return render(request, 'school_app/contact.html')


def notices_list(request):
    """
    Notices listing page view.

    Displays all active notices with their PDF download links.
    Notices are managed through the Django admin panel - no code changes needed.

    Context:
        notices: QuerySet of all active notices, ordered by date (newest first)
    """
    notices = Notice.objects.filter(is_active=True)
    return render(request, 'school_app/notices.html', {'notices': notices})
