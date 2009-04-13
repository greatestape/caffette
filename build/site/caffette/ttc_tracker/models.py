import datetime
import urllib
from xml.etree import ElementTree

from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _

from myttc_api import MyTTCStop
from ttc_tracker import settings as tracker_settings


class Stop(models.Model):
    """A TTC stop with stop times pulled from myttc"""
    name = models.CharField(max_length=255, verbose_name=_("name"))
    myttc_url = models.URLField(verify_exists=True, verbose_name=_('myttc url'),
            help_text=_('URL of stop\'s XML representation'))

    class Meta:
        verbose_name = _("Stop")
        verbose_name_plural = _("Stops")

    def __unicode__(self):
        return self.name

    @property
    def cache_key(self):
        return 'ttc_tracker_stop__%s' % self.myttc_url

    @property
    def next_arrivals(self):
        return [route['stop_times'][0] for route in self.routes.values()]

    @property
    def routes(self):
        routes = cache.get(self.cache_key)
        if routes is None:
            routes = self._get_routes_from_myttc()
            cache.set(self.cache_key, routes, tracker_settings.ROUTE_CACHE_TIMEOUT)
        return routes

    def _get_routes_from_myttc(self):
        response = urllib.urlopen(self.myttc_url)
        return self._get_routes_from_xml(ElementTree.parse(response))

    def _get_routes_from_xml(self, xml):
        routes = {}
        for route_xml in xml.findall('stop/routes/route'):
            stop_times = []
            for stop_time_xml in route_xml.findall('stoptimes/stoptime'):
                stop_times.append({
                        'route_name': stop_time_xml.find('route').text,
                        'when': datetime.datetime.fromtimestamp(
                                float(stop_time_xml.find('time').attrib['timestamp'])
                                ),
                        })
            routes.setdefault(route_xml.attrib['uri'], {
                    'name': route_xml.find('name').text,
                    'stop_times': stop_times,
                    })
        return routes