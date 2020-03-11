from __future__ import print_function, unicode_literals
from clldutils.path import Path
#from clld.tests.util import TestWithApp

import gelato

import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/contributions/pembertonautosomalstr'),
        ('get_html', '/parameters/pembertonautosomalstr-heterozygosity'),
        ('get_html', '/languages/humanoriginsautosomalsnp-26'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
