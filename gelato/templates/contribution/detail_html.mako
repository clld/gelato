<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<h2>${_('Contribution')} ${ctx.name}</h2>

<div>
    ${ctx.formatted_description|n}
</div>


<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#samples" data-toggle="tab">Samples</a></li>
        <li><a href="#measures" data-toggle="tab">Measures</a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="samples" class="tab-pane active">
            ${request.get_datatable('languages', h.models.Language, panel=ctx).render()}
        </div>
        <div id="measures" class="tab-pane">
            ${request.get_datatable('parameters', h.models.Parameter, panel=ctx).render()}
        </div>
    </div>
    <script>
$(document).ready(function() {
    if (location.hash !== '') {
        $('a[href="#' + location.hash.substr(2) + '"]').tab('show');
    }
    return $('a[data-toggle="tab"]').on('shown', function(e) {
        return location.hash = 't' + $(e.target).attr('href').substr(1);
    });
});
    </script>
</div>
