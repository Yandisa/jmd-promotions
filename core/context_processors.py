from .models import SiteSettings, Announcement

def site_settings(request):
    settings = SiteSettings.get()
    announcements = Announcement.objects.filter(active=True)
    return {
        'site': settings,
        'announcements': announcements,
    }
