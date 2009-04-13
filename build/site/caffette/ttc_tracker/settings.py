from django.conf import settings


ROUTE_CACHE_TIMEOUT = getattr(settings, 'TTC_TRACKER_ROUTE_CACHE_TIMEOUT', 300)
