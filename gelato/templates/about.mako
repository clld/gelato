<%inherit file="home_comp.mako"/>

<h2>About GELATO</h2>

<h3>Credits</h3>
<p>GeLaTo was created by Chiara Barbieri, Damián Blasi and Robert Forkel.</p>
<div style="float: right; width: 28%">
    <img class="img-polaroid" src="${request.static_url('gelato:static/gelatauro.png')}" />
</div>
<dl style="width: 70%">
    <dt>Chiara Barbieri:</dt><dd>genetic data curation, population genetics analysis, database assembly.</dd>
    <dt>Damián Blasi:</dt><dd>conceptualization, project name.</dd>
    <dt>Robert Forkel:</dt><dd>database structure, data curation and web interface.</dd>
</dl>

<p>The concept of GeLaTo was developed from conversations at the Department of Linguistic and Cultural Evolution at the Max Planck Institute for the Science of Human History, Jena, Germany, and the dataset was assembled at the University of Zurich.</p>
<p>Concept supervision: Russell Gray, Balthasar Bickel, Kentaro Shimizu.</p>
<p>The curation of the dataset for glottocode assignation was performed by Barbieri, Blasi and Forkel with the expertise of Harald Hammarström, and the support of various contributors: Søren Wichmann, Simon J. Greenhill, Balthasar Bickel, Russell Gray, Natalia Chousou-Polydouri, Paul Heggarty, Tom Güldemann, Matthias Urban, Brigitte Pakendorf, Jessica Ivani, Kellen Parker van Dam, Anne-Maria Fehn, Hiba Babiker, Nora Muheim.</p>
<p>Details on the contribution for each genetic population is listed in the ${h.external_link("https://github.com/gelato-org/gelato-data/blob/master/datasets/HumanOrigins_AutosomalSNP/samples.csv", label="dataset curation notes")}.</p>
<p>Chiara Barbieri was supported by funds from the
    ${h.external_link("https://www.evolution.uzh.ch/en.html", label="URPP Evolution in Action")} program of the University of Zurich and from the
    ${h.external_link("https://evolvinglanguage.ch/", label="NCCR Evolving Language")} grant of the Swiss National Science Fundation.</p>

<h3>Contributing</h3>
<p>Glottolog data is curated in a public repository at  https://github.com/gelato-org/gelato-data. We welcome suggestions for:</p>
<ul>
    <li>improving the glottocode matches to the genetic populations</li>
    <li>suggesting genetic publications to include, which satisfy the following criteria: data compatible to the genetic panels considered, and population samples with an anthropological/linguistic background description</li>
    <li>suggesting new genetic analysis and variables to compute over the dataset</li>
</ul>

<h3>Publications</h3>
<p>Academic publications which deal with GeLaTo include:</p>
<ul>
    <li>${req.dataset.jsondata['citation']}</li>
</ul>
