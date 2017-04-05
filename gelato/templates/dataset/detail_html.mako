<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    ##<div class="well">
        ##<h3>Sidebar</h3>
        <p>
            <img class="image" src="${request.static_url('gelato:static/gelato_logo.png')}" />
        </p>
    ##</div>
</%def>

<h2>GELATO: GEnes and LAnguages TOgether</h2>

<p>
    The GeLaTo dataset is a worldwide diversity panel of available population genetic samples
    matched with databases of linguistic, cultural and environmental diversity. Population genetic
    samples are assigned to existing GlottoCodes, following ethnolinguistic criteria: the data is
    filtered following the indication of geneticists, linguists, cultural anthropologists and historians.
    The choice of genetic data corresponds to essential guidelines: maximum compatibility and
    standardization, modern high quality data, avoidance of ascertainment bias, availability for
    different regions of the world, and finally high resolution to capture recent events. The dataset
    provides elaborated summary statistics such as genetic diversity within a population, genetic proximity
    between pairs of populations, sharing of identical motifs, and demographic history reconstructions. The
    genetic samples are directly linked to Glottolog and D-Place databases, and to the original publication.
    The current version hosts summary statistics from the genetic diversity panel of autosomal STR from
    ${h.external_link('https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3656735/', label='Pemberton et al. 2013')}
    It will be expanded to include mtDNA genomes, Y chromosome STRs, and autosomal SNPs.
</p>
<p>
GeLaTo goals:
</p>
<ul>
    <li>Allowing geneticists to properly characterize the human history behind the molecular data, and give an accessible reference dataset for regional or worldwide comparisons.</li>
    <li>Allowing linguists, historians and cultural anthropologists to integrate information on genealogical relatedness and demography, which can be robustly extrapolated from the genetic data.</li>
    <li>Allowing scholars of various disciplines to approach questions of major relevance on human diversity in a true multidisciplinary perspective, and develop a more realistic understanding of the complex mechanisms behind human migration, contact and cultural transmission.</li>
</ul>
<p>
    <small>
        Icons made by
        ${h.external_link('http://www.freepik.com', label='Freepik')}
        from
        ${h.external_link('http://www.flaticon.com', label='www.flaticon.com')}
        are licensed under
        ${h.external_link('http://creativecommons.org/licenses/by/3.0/', label='CC 3.0 BY')}
    </small>
</p>