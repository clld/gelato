import sys
from itertools import cycle
from colorsys import hsv_to_rgb

from sqlalchemy.orm import joinedload
from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.web.icon import ORDERED_ICONS
from clldutils.path import Path, as_unicode, read_text
from clldutils.misc import slug
from csvw.dsv import reader
from pyglottolog.api import Glottolog

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
    repos = Path(__file__).parent.resolve().parent.parent.parent.joinpath('gelato-data')
    print(repos)
    assert repos.exists()
    data = Data()

    glottolog = Glottolog(repos.parent.parent / 'glottolog' / 'glottolog')
    languoids = {l.id: l for l in glottolog.languoids()}
    icons = cycle(ORDERED_ICONS)

    dataset = common.Dataset(
        id=gelato.__name__,
        name="GeLaTo",
        description="Genes and Languages together",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://www.shh.mpg.de",
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

    for dsdir in repos.joinpath('datasets').iterdir():
        if not dsdir.is_dir():
            continue

        ds = data.add(
            models.Panel,
            dsdir.name,
            id=slug(as_unicode(dsdir.name)),
            name=dsdir.name,
            description=read_text(dsdir / 'README.md'),
        )
        # samples.csv:
        #SamplePopID,populationName,samplesize,geographicRegion,dataSet.of.origin,lat,lon,location,languoidName,glottocode,curation_notes,Exclude
        for row in reader(dsdir.joinpath('samples.csv'), encoding='macroman', dicts=True):
            if row['glottocode'] == 'NA':
                continue

            lang = data['Languoid'].get(row['glottocode'])
            if not lang:
                if row['glottocode'] not in languoids:
                    continue
                gl_lang = languoids[row['glottocode']]
                gl_family = gl_lang.family or gl_lang
                icon = families.get(gl_family.id)
                if not icon:
                    families[gl_family.id] = icon = next(icons)
                lang = data.add(
                    models.Languoid,
                    row['glottocode'],
                    id=row['glottocode'],
                    name=gl_lang.name,
                    family_id=gl_family.id,
                    family_name=gl_family.name,
                    jsondata=dict(icon=icon.name),
                )
            data.add(
                models.Sample,
                row['SamplePopID'],
                id='{0}-{1}'.format(ds.id, row['SamplePopID']),
                name=row['populationName'],
                panel=ds,
                languoid=lang,
                latitude=float(row['lat']) if row['lat'] != 'NA' else None,
                longitude=float(row['lon']) if row['lon'] != 'NA' else None,
                samplesize=int(row['samplesize']),
                source=row.get('dataSet.of.origin'),
                region=row['geographicRegion'],
                location=row['location'],
                jsondata=dict(color=REGIONS[row['geographicRegion']]),
            )

        #VarID,Variable name,Description,Source
        for row in reader(dsdir.joinpath('variables.csv'), dicts=True):
            data.add(
                models.Measure,
                row['VarID'],
                id='{0}-{1}'.format(ds.id, row['VarID']),
                name=row['Variable name'],
                description=row['Description'],
                panel=ds)

        # data.csv
        #SamplePopID,populationName,ExpectedHeterozygosity,residuals
        for i, row in enumerate(reader(dsdir.joinpath('data.csv'), dicts=True, delimiter=';')):
            sample = data['Sample'].get(row['SamplePopID'])
            if not sample:
                continue
            for pid in row:
                param = data['Measure'].get(pid)
                if not param:
                    continue

                if row[pid] == 'NA':
                    continue

                vs = data.add(
                    common.ValueSet,
                    i,
                    id='{0}-{1}-{2}'.format(ds.id, param.id, i + 1),
                    language=sample,
                    parameter=param,
                    contribution=ds,
                    jsondata=dict(color=REGIONS[sample.region]),
                )
                data.add(
                    models.Measurement,
                    i,
                    id='{0}-{1}-{2}'.format(ds.id, param.id, i + 1),
                    valueset=vs,
                    name='{0:.2}'.format(float(row[pid])),
                    value=float(row[pid]))


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
        minval = min(vs.values[0].value for vs in p.valuesets)
        maxval = max(vs.values[0].value for vs in p.valuesets)
        for vs in p.valuesets:
            vs.values[0].jsondata = vs.jsondata = {'icon': 's' + color(minval, maxval, vs.values[0].value)}


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
