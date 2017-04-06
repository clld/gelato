<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

<table class="table table-nonfluid table-condensed">
    <tbody>
        <tr>
            <th>Sample size</th>
            <td>${ctx.samplesize}</td>
        </tr>
        <tr>
            <th>Region</th>
            <td>${ctx.region}</td>
        </tr>
        <tr>
            <th>Glottolog variety</th>
            <td>${h.external_link('http://glottolog.org/resource/languoid/id/' + ctx.languoid.id, label=ctx.languoid.name)}</td>
        </tr>
        <tr>
            <th>Glottolog family</th>
            <td>
                % if ctx.languoid.id != ctx.languoid.family_id:
                    ${h.external_link('http://glottolog.org/resource/languoid/id/' + ctx.languoid.family_id, label=ctx.languoid.family_name)}
                % else:
                    <em>Isolate</em>
                % endif
            </td>
        </tr>
    </tbody>
</table>

<h3>Measurements</h3>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    ${util.language_meta()}
</%def>
