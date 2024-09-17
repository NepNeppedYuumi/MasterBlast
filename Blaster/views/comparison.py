# Third-party imports
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

# Local imports
from Blaster.models import BlastHit
from Blaster.utils.bokeh import seqlen_graph, perc_identity_graph, \
    query_coverage_graph, e_value_graph


def comparison_page(request: WSGIRequest) -> HttpResponse:
    """Renders the comparison page

    Takes the selected hits from the BLAST hit page and creates four
    graphs with the data from the selected hits.
    All graphs are generated in utils/bokeh.py and are returned as 
    scripts and divs that are embedded in the comparison template.

    :param request: Django request object
    :type request: WSGIRequest
    :return: Comparison page or 500 page if no hits are selected
    :rtype: HttpResponse
    """
    if not request.session.get('selected_hits'):
        return render(request, '500.html')

    hit_ids = request.session.get('selected_hits')
    hit_ids = [int(id) for id in hit_ids]
    hits = BlastHit.objects.filter(id__in=hit_ids)

    lengths, graphs = [], {}

    # Get the sequence length of every hit
    for hit in hits:
        lengths.append(len(hit.subject_seq))

        hit.unique_accession = f'{hit.accession.code}.{hit.id}'

    seqlen_script, seqlen_div = seqlen_graph(hits)
    perc_identity_script, perc_identity_div = perc_identity_graph(hits)
    query_coverage_script, query_coverage_div = query_coverage_graph(hits)
    e_value_script, e_value_div = e_value_graph(hits)
    
    graphs['seqlen'] = {
        'script': seqlen_script, 
        'div': seqlen_div
        }
    graphs['perc_identity'] = {
        'script': perc_identity_script, 
        'div': perc_identity_div
        }
    graphs['query_coverage'] = {
        'script': query_coverage_script, 
        'div': query_coverage_div
        }
    graphs['e_value'] = {
        'script': e_value_script, 
        'div': e_value_div
        }

    context = {
        'selected_hits': hits,
        'graphs': graphs,
    }
    return render(request, 'pages/comparison.html', context)
