from __future__ import unicode_literals

from sqlalchemy.orm import joinedload
from clld.web.maps import ParameterMap, Map, FilterLegend, Layer
from clld.web.adapters.geojson import GeoJsonLanguages
from clld.db.meta import DBSession

from gelato.models import Panel


class MeasureMap(ParameterMap):
    def get_options(self):
        return {'icon_size': 15}


class PanelSamples(GeoJsonLanguages):
    def feature_iterator(self, ctx, req):
        return ctx.samples


class SamplesMap(Map):
    def __init__(self, ctx, req, eid='map', col=None, dt=None):
        self.col, self.dt = col, dt
        Map.__init__(self, ctx, req, eid=eid)

    def get_layers(self):
        for panel in DBSession.query(Panel).options(joinedload(Panel.samples)):
            yield Layer(
                panel.id,
                panel.name,
                PanelSamples(None).render(panel, self.req, dump=False),
            )


    def get_legends(self):
        for legend in super(SamplesMap, self).get_legends():
            yield legend
        yield FilterLegend(self, 'GELATO.getFamily', col=self.col, dt=self.dt)

    def get_options(self):
        return {'icon_size': 15}


def includeme(config):
    config.register_map('parameter', MeasureMap)
    config.register_map('languages', SamplesMap)
