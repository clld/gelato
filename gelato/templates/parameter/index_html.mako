<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameters')}</%block>

<h2>Genetic summary statistics available in GeLaTo</h2>

<p>
The current release of GeLaTo provides genetic summary statistics based on pairwise genetic distances.
These are calculated as FST using the method introduced in
<strong>Weir BS, Cockerham CC (1984) Estimating F-statistics for the analysis of population structure</strong>.
</p>
<p>
FST distances are used to infer rough population divergence times. Divergence time between two populations
(as generations ago) is extrapolated from FST, being proportional to the effective population size (Ne) with
a formula equivalent to <i>Time = 2Ne * linearized FST</i>
(<strong>M. Nei, Molecular evolutionary genetics. Columbia University Press, 1987</strong>). Divergence time in
year is calculated with a generation time of 29 years.
</p>
<p>
Effective population size Ne is calculated with IBDNe
(<strong>S. R. R. Browning, B. L. L. Browning, Accurate Non-parametric Estimation of Recent Effective Population Size from Segments of Identity by Descent. Am. J. Hum. Genet. 97, 404–418 (2015)</strong>),
which is based on Identity By Descent block coalescent. From the size and the number of Identity by Descent
blocks it is possible to reconstruct the number of shared ancestors and infer variation in Ne through time.
Identity by Descent blocks are retrieved after phasing the data with Beagle and running refinedIBD and its
associate tools for gap removals (**B. L. Browning, S. R. Browning, Improving the accuracy and efficiency of
identity-by-descent detection in population data. Genetics 194, 459–471 (2013).**). The harmonic mean of the
last 50 generations was used to approximate Ne (this would minimize the effect of increase or decline in the
last 10-20 generations). Populations with an Ne >10,000 were not considered (such high Ne can be resulting
from population substructure and are not compatible with estimates coming from whole genome data). Ne values
were considered for the following analysis only if the reconstructed profile was relatively stable in time,
without large increase or decline (populations with a difference in Ne through generations of more than 10,000
were excluded). Populations with very large confidence intervals and continuous increase/decline were then further
excluded. Divergence time estimates are available only for pairs of populations for which it is possible to calculate the Ne.
</p>
<div class="alert alert-warn">
    This web application only lists parameters with scalar datatypes. To access the other parameters (listed
    with datatype <span style="font-family: monospace">"json"</span> <a href="https://github.com/gelato-org/gelato-data/blob/master/cldf/variables.csv">in the dataset</a>),
    please <a href="${req.route_url('download')}">download the dataset</a>.
</div>

<div>
    ${ctx.render()}
</div>
