<%inherit file="home_comp.mako"/>
<%namespace name="mpg" file="clldmpg_util.mako"/>

<h3>${_('Downloads')}</h3>

<div class="alert alert-info">
    <p>
        The GeLaTo web application serves the latest
        ${h.external_link('https://github.com/gelato-org/gelato-data/releases', label=_('released version'))}
        of data curated at
        ${h.external_link('https://github.com/gelato-org/gelato-data', label='gelato-org/gelato')}.
        All released version are accessible via
        <a href="https://doi.org/10.5281/zenodo.7233266">
            <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.7233266.svg" alt="DOI">
        </a>
        <br/>
        on ZENODO as well.
    </p>
</div>
<h4>How to cite</h4>
<p>If you use this data, please cite</p>
<blockquote>
    ${req.dataset.jsondata['citation']}
</blockquote>
<p>as well as the exact released version of the dataset.</p>
