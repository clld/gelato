from __future__ import print_function, unicode_literals
from clldutils.path import Path
#from clld.tests.util import TestWithApp

import gelato

import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
