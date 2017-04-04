# coding: utf8
from __future__ import unicode_literals
import sys

from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clldutils.path import Path, as_unicode
from clldutils.misc import slug
from clldutils.dsv import reader

import gelato
from gelato import models


def main(args):
    repos = Path(__file__).parent.resolve().parent.parent.parent.joinpath('gelato-data')
    print(repos)
    assert repos.exists()
    data = Data()

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

    for dsdir in repos.joinpath('datasets').iterdir():
        if not dsdir.is_dir():
            continue

        ds = data.add(common.Contribution, dsdir.name, id=slug(as_unicode(dsdir.name)), name=dsdir.name)
        # samples.csv:
        #SamplePopID,populationName,samplesize,geographicRegion,dataSet.of.origin,lat,lon,location,languoidName,glottocode,curation_notes,Exclude
        for row in reader(dsdir.joinpath('samples.csv'), dicts=True):
            data.add(
                common.Language,
                row['SamplePopID'],
                id=row['SamplePopID'],
                name=row['populationName'],
                latitude=float(row['lat']),
                longitude=float(row['lon']),
            )

        # data.csv
        #SamplePopID,populationName,ExpectedHeterozygosity,residuals
        for i, row in enumerate(reader(dsdir.joinpath('data.csv'), dicts=True)):
            sample = data['Language'][row['SamplePopID']]
            for pid in row:
                if pid in ['SamplePopID', 'populationName']:
                    continue
                param = data['Parameter'].get(pid)
                if not param:
                    param = data.add(common.Parameter, pid, id=slug(pid), name=pid)

                vs = data.add(
                    common.ValueSet,
                    i,
                    id='{0}-{1}-{2}'.format(ds.id, pid, i + 1),
                    language=sample,
                    parameter=param,
                    contribution=ds,
                )
                data.add(
                    common.Value,
                    i,
                    id='{0}-{1}-{2}'.format(ds.id, pid, i + 1),
                    valueset=vs,
                    name='{0}'.format(row[pid]))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
