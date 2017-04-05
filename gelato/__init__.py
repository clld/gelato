from pyramid.config import Configurator

from clld import interfaces
from clld.web.icon import MapMarker

# we must make sure custom models are known at database initialization!
from gelato import models


_ = lambda s: s
_('Contribution')
_('Contributions')
_('Language')
_('Languages')
_('Parameter')
_('Parameters')
_('Value')
_('Values')


class GelatoMapMarker(MapMarker):
    def __call__(self, ctx, req):
        icon = None

        if interfaces.ILanguage.providedBy(ctx) or interfaces.IValueSet.providedBy(ctx):
            return req.registry.getUtility(interfaces.IIcon, 'c{0}'.format(ctx.jsondata['color'])).url(req)

        return super(GelatoMapMarker, self).__call__(ctx, req)  # pragma: no cover


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.registry.registerUtility(GelatoMapMarker(), interfaces.IMapMarker)
    return config.make_wsgi_app()
