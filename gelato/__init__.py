from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from gelato import models


_ = lambda s: s
_('Contribution')
_('Contributions')
_('Language')
_('Languages')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    return config.make_wsgi_app()
