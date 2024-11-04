<%inherit file="app.mako"/>

<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}"
       style="padding-top: 7px; padding-bottom: 2px;">
        <img width="20" src="${request.static_url('gelato:static/logo.png')}"/>
        ${request.dataset.name}
    </a>
</%block>

<%block name="footer">
    <div class="row-fluid" style="padding-top: 15px; border-top: 1px solid black;">
        <div class="span2">
            <a href="http://www.comparativelinguistics.uzh.ch"
               title="Department of Comparative Linguistics - University of Zurich">
                <img width="220" src="${request.static_url('gelato:static/UZH_logo.jpg')}" />
            </a>
        </div>
        <div class="span2">
            <a href="https://evolvinglanguage.ch/"
               title="evolving language - National Centre of Competence in Research">
                <img width="200" src="${request.static_url('gelato:static/EvoLang.png')}" />
            </a>
        </div>
        <div class="span4" style="text-align: center;">
            <% license_icon = h.format_license_icon_url(request) %>
            % if license_icon:
            <a rel="license" href="${request.dataset.license}">
                <img alt="License" style="border-width:0" src="${license_icon}" />
            </a>
            <br />
            % endif
            ${request.dataset.formatted_name()}
            edited by
            <span xmlns:cc="http://creativecommons.org/ns#"
                  property="cc:attributionName"
                  rel="cc:attributionURL">
                ${request.dataset.formatted_editors()}
           </span>
            <br />
            is licensed under a
            <a rel="license" href="${request.dataset.license}">
                ${request.dataset.jsondata.get('license_name', request.dataset.license)}
            </a>.
        </div>
        <div class="span4" style="text-align: right">
            <a href="https://www.eva.mpg.de/linguistic-and-cultural-evolution/index/"
               title="${request.dataset.publisher_name}, ${request.dataset.publisher_place}">
                % if request.registry.settings.get('clld.publisher_logo'):
                    <img width="80" src="${request.static_url(request.registry.settings['clld.publisher_logo'])}" />
                % else:
                ${request.dataset.publisher_name}, ${request.dataset.publisher_place}
                % endif
            </a>
        </div>
    </div>
</%block>


${next.body()}
