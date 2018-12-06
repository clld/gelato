from __future__ import unicode_literals, print_function, division

from sqlalchemy.orm import joinedload
from clld.web.datatables.base import LinkCol, LinkToMapCol, Col
from clld.web.datatables.language import Languages
from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.contribution import Contributions
from clld.db.util import get_distinct_values
from clld.web.util.htmllib import HTML
from clld.db.models.common import Parameter

from gelato.models import Sample, Measurement, Languoid, Panel, Measure


class LangCol(Col):
    def format(self, item):
        return HTML.a(item.languoid.name, href="http://glottolog.org/resource/languoid/id/" + item.languoid.id)


class FamilyCol(Col):
    def format(self, item):
        item = self.get_obj(item)
        return HTML.span(
            HTML.img(
                width='20',
                src=self.dt.req.static_url(item.jsondata['icon'])),
            ' ',
            HTML.a(item.family_name, href="http://glottolog.org/resource/languoid/id/" + item.family_id),
            style="white-space: nowrap;")


class Samples(Languages):
    __constraints__ = [Panel]

    def base_query(self, query):
        query = query.join(Sample.panel)
        if self.panel:
            query = query.filter(Panel.pk == self.panel.pk)
        return query.join(Languoid).options(joinedload(Sample.languoid))

    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            LinkToMapCol(self, '#'),
            Col(self, 'region', model_col=Sample.region, choices=get_distinct_values(Sample.region)),
            Col(self, 'location', model_col=Sample.location),
            Col(self,
                'latitude',
                input_size='mini',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                input_size='mini',
                sDescription='<small>The geographic longitude</small>'),
            Col(self, 'samplesize', input_size='mini', model_col=Sample.samplesize),
            LangCol(self, 'languoid', get_object=lambda i: i.languoid, model_col=Languoid.name),
            FamilyCol(self, 'family', get_object=lambda i: i.languoid, model_col=Languoid.family_name, choices=get_distinct_values(Languoid.family_name)),
        ]


class Measures(Parameters):
    __constraints__ = [Panel]

    def base_query(self, query):
        query = query.join(Measure.panel)
        if self.panel:
            query = query.filter(Panel.pk == self.panel.pk)
        return query

    def col_defs(self):
        res = [
            LinkCol(self, 'name'),
            Col(self, 'description'),
        ]
        if not self.panel:
            res.append(LinkCol(self, 'panel', get_object=lambda i: i.panel))
        return res


class Measurements(Values):
    def base_query(self, query):
        query = Values.base_query(self, query)
        if self.parameter:
            query = query.join(Sample.languoid)
        return query

    def col_defs(self):
        if self.parameter:
            return [
                LinkCol(self, 'sample', model_col=Sample.name, get_object=lambda i: i.valueset.language),
                Col(self,
                    'region',
                    model_col=Sample.region,
                    get_object=lambda i: i.valueset.language,
                    format=lambda i: i.valueset.language.region),
                FamilyCol(self, 'family', get_object=lambda i: i.valueset.language.languoid, model_col=Languoid.family_name, choices=get_distinct_values(Languoid.family_name)),
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


class Panels(Contributions):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'description', format=lambda i: i.formatted_description),
        ]


def includeme(config):
    config.register_datatable('languages', Samples)
    config.register_datatable('values', Measurements)
    config.register_datatable('parameters', Measures)
    config.register_datatable('contributions', Panels)
