from pyramid.config import Configurator

from clld.interfaces import IMapMarker, ILanguage, IIcon, IValueSet, IValue
from clld.web.icon import MapMarker
from clld.lib import svg

# we must make sure custom models are known at database initialization!
from gelato import models
from gelato.interfaces import ILanguoid


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
        #if ILanguage.providedBy(ctx) or IValueSet.providedBy(ctx):
        #    return req.registry.getUtility(IIcon, 'c{0}'.format(ctx.jsondata['color'])).url(req)
        icon = None
        if ILanguage.providedBy(ctx):
            icon = ctx.languoid.jsondata['icon']
        elif IValue.providedBy(ctx):
            icon = ctx.jsondata['icon']
        elif IValueSet.providedBy(ctx):
            icon = ctx.jsondata['icon']
        if icon:
            try:
                return svg.data_url(svg.icon(icon))
            except:
                raise ValueError(icon)

        return super(GelatoMapMarker, self).__call__(ctx, req)  # pragma: no cover


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.registry.registerUtility(GelatoMapMarker(), IMapMarker)
    config.register_resource('languoid', models.Languoid, ILanguoid, with_index=True)
    return config.make_wsgi_app()
