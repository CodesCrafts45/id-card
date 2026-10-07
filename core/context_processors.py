from .models import EventSettings, DeveloperCard


def site_settings(request):
    try:
        settings = EventSettings.get_solo()
    except Exception:
        settings = None
    try:
        developer = DeveloperCard.get_solo()
    except Exception:
        developer = None
    return {
        "site_settings": settings,
        "developer_card": developer,
    }
