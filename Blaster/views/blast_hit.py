# Third-party imports
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest

# Local imports
from Blaster.utils.ncbi import get_entrez_db_from_blast_program, \
    query_and_create_entrez_accession_cache
from Blaster.utils.queries import get_blast_hit_from_id


def blast_hit_page(request: WSGIRequest, blast_hit_id: int) -> HttpResponse:
    """Render the BLAST hit page.

    Takes a BlastHit id and retrieves its object from the database.
    Checks if the user is not authenticated or the hit is not valid 
    and renders 403 and 404, respectively. Retrieves and stores a hit's
    EntrezAccessionCache object, then renders these in blast_hit.html.

    :param request: Django request object.
    :type request: WSGIRequest.
    :param blast_hit_id: identifier for the BlastHit to be rendered.
    :type blast_hit_id: int.
    :return: BLAST hit page.
    :rtype: HttpResponse.
    """
    try:
        hit = get_blast_hit_from_id(blast_hit_id)
    except (Http404, ValueError):
        return render(request, '404.html', status=404)

    if hit.job.user is not None and hit.job.user != request.user:
        return render(request, '403.html', status=403)

    db = get_entrez_db_from_blast_program(hit.job.program)
    if not hit.accession.cache:
        cache = query_and_create_entrez_accession_cache(hit.accession.code, db)
        hit.accession.cache = cache
        hit.accession.save()

    context = {
        'hit': hit,
        'genbank': hit.accession.cache.genbank,
        'fasta': hit.accession.cache.fasta
    }
    return render(request, 'pages/blast_hit.html', context)
