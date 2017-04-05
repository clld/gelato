from __future__ import unicode_literals, print_function, division

from clld.web.datatables.base import LinkCol, LinkToMapCol, Col
from clld.web.datatables.language import Languages
from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.db.util import get_distinct_values
from clld.web.util.htmllib import HTML
from clld.db.models.common import Parameter

from gelato.models import Sample, Measurement


class LangCol(Col):
    def format(self, item):
        return HTML.a(item.lang_name, href="http://glottolog.org/resource/languoid/id/" + item.lang_glottocode)


class Samples(Languages):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            LinkToMapCol(self, '#'),
            Col(self, 'region', model_col=Sample.region, choices=get_distinct_values(Sample.region)),
            Col(self, 'location', model_col=Sample.location),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
            Col(self, 'samplesize', model_col=Sample.samplesize),
            LangCol(self, 'languoid', model_col=Sample.lang_name),
        ]


class Measures(Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'description'),
        ]


class Measurements(Values):
    def col_defs(self):
        if self.parameter:
            return [
                LinkCol(self, 'sample', model_col=Sample.name, get_object=lambda i: i.valueset.language),
                Col(self, 'region', get_object=lambda i: i.valueset.language, format=lambda i: i.valueset.language.region),
                Col(self, 'value', model_col=Measurement.value),
                LinkToMapCol(self, '#', get_object=lambda i: i.valueset.language),
            ]
        if self.language:
            return [
                LinkCol(self, 'measure', model_col=Parameter.name, get_object=lambda i: i.valueset.parameter),
                Col(self, 'description', get_object=lambda i: i.valueset.parameter, model_col=Parameter.description),
                Col(self, 'value', model_col=Measurement.value),
            ]
        return Values.col_defs(self)


def includeme(config):
    config.register_datatable('languages', Samples)
    config.register_datatable('values', Measurements)
    config.register_datatable('parameters', Measures)
