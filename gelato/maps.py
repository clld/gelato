from __future__ import unicode_literals

from clld.web.maps import ParameterMap, Map, FilterLegend


class MeasureMap(ParameterMap):
    def get_options(self):
        return {'icon_size': 15}


class SamplesMap(Map):
    def __init__(self, ctx, req, eid='map', col=None, dt=None):
        self.col, self.dt = col, dt
        Map.__init__(self, ctx, req, eid=eid)

    def get_legends(self):
        for legend in super(SamplesMap, self).get_legends():
            yield legend
        yield FilterLegend(self, 'GELATO.getFamily', col=self.col, dt=self.dt)

    def get_options(self):
        return {'icon_size': 15}


def includeme(config):
    config.register_map('parameter', MeasureMap)
    config.register_map('languages', SamplesMap)
