<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">Genetic Samples</%block>


<h2>Genetic Samples</h2>

${request.get_map('languages', col='family', dt=ctx).render()}

<div>
    ${ctx.render()}
</div>
