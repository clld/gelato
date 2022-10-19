from itertools import cycle
from colorsys import hsv_to_rgb

from sqlalchemy.orm import joinedload
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.web.icon import ORDERED_ICONS
from clld.lib import bibtex
from csvw import Datatype

import gelato
from gelato import models

REGIONS = {
    'EAST_ASIA': '0000ff',
    'SOUTHEAST_ASIA': '0000ff',
    'AFROEUROPEAN': '00ff00',
    'LATINO': 'ff0000',
    'MIDDLE_EAST': '00ffff',
    'CENTRAL_SOUTH_ASIA': 'ff00ff',
    'AFRICA': 'ffff00',
    'EUROPE': '000000',
    'EURASIA': '000000',
    'AMERICA': 'cccccc',
    'AMERICAS': 'cccccc',
    'OCEANIA': 'ffffff',
}

def main(args):
    data = Data()

    icons = cycle(ORDERED_ICONS)

    dataset = common.Dataset(
        id=gelato.__name__,
        name="GeLaTo",
        description="Genes and Languages together",
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="https://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='gelato.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})

    for i, (id_, name) in enumerate([
        ('barbierichiara', 'Chiara Barbieri'),
        ('blasidamian', 'Damián Blasi'),
        ('forkelrobert', 'Robert Forkel')
    ]):
        ed = data.add(common.Contributor, id_, id=id_, name=name)
        common.Editor(dataset=dataset, contributor=ed, ord=i + 1)

    families = {}

    for rec in bibtex.Database.from_file(args.cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    for r in args.cldf.iter_rows('ContributionTable', 'id', 'name', 'description'):
        ds = data.add(
            models.Panel, r['id'], id=r['id'], name=r['name'], description=r['description'])
    for row in args.cldf.iter_rows('LanguageTable', 'id', 'name', 'contributionReference'):
        icon = families.get(row['LanguageFamily_Glottocode'])
        if not icon:
            families[row['LanguageFamily_Glottocode']] = icon = next(icons)
        lang = data['Languoid'].get(row['Glottocode'])
        if not lang:
            lang = data.add(
                models.Languoid,
                row['Glottocode'],
                id=row['Glottocode'],
                name=row['Language_Name'],
                family_id=row['LanguageFamily_Glottocode'],
                family_name=row['LanguageFamily'],
                jsondata=dict(icon=icon.name),
            )
        s = data.add(
            models.Sample,
            row['id'],
            id=row['id'],
            name=row['Name'],
            panel=data['Panel'][row['contributionReference']],
            languoid=lang,
            latitude=row['Latitude'],
            longitude=row['Longitude'],
            samplesize=int(row['samplesize']),
            region=row['geographicRegion'],
            location=row['country'],
            jsondata=dict(color=REGIONS[row['geographicRegion']]),
        )
        DBSession.flush()
        for bibkey in row['Source']:
            DBSession.add(
                common.LanguageSource(language_pk=s.pk, source_pk=data['Source'][bibkey].pk))

    types = {}
    for row in args.cldf.iter_rows(
            'ParameterTable', 'id', 'name', 'description', 'contributionReference'):
        types[row['id']] = Datatype.fromvalue(row['datatype'])
        if types[row['id']].base in ['float', 'integer']:
            data.add(
                models.Measure,
                row['id'],
                id=row['id'],
                name=row['name'],
                description=row['description'],
                panel=data['Panel'][row['contributionReference']])

    for row in args.cldf.iter_rows('ValueTable', 'id', 'parameterReference', 'languageReference'):
        v = types[row['parameterReference']].read(row['Value'])
        if isinstance(v, (float, int)):
            vs = data.add(
                common.ValueSet,
                row['id'],
                id=row['id'],
                language=data['Sample'][row['languageReference']],
                parameter=data['Measure'][row['parameterReference']],
                #contribution=ds,
                #jsondata=dict(color=REGIONS[sample.region]),
            )
            data.add(
                models.Measurement,
                row['id'],
                id=row['id'],
                valueset=vs,
                name=row['Value'],
                value=v)


def color(minval, maxval, val):  # pragma: no cover
    """ Convert val in range minval..maxval to the range 0..120 degrees which
        correspond to the colors Red and Green in the HSV colorspace.
    """
    h = 120 - (float(val-minval) / (maxval-minval)) * 120

    # Convert hsv color (h,1,1) to its rgb equivalent.
    # Note: hsv_to_rgb() function expects h to be in the range 0..1 not 0..360
    return ''.join("{0:02x}".format(int(255*n)) for n in hsv_to_rgb(h/360, 1., 1.))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for p in DBSession.query(common.Parameter).options(
            joinedload(common.Parameter.valuesets).joinedload(common.ValueSet.values)):
        if p.valuesets:
            minval = min(vs.values[0].value for vs in p.valuesets)
            maxval = max(vs.values[0].value for vs in p.valuesets)
            for vs in p.valuesets:
                vs.values[0].jsondata = vs.jsondata = {'icon': 's' + color(minval, maxval, vs.values[0].value)}
