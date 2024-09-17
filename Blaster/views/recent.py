# Third-party imports
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.functions import Length
from django.http import HttpResponse
from django.shortcuts import render

# Local imports
from Blaster.models import BlastJob


@login_required()
def recent_page(request: WSGIRequest) -> HttpResponse:
    """Renders the recent jobs page

    Shows the 10 most recent jobs of the logged in user by default.
    Sorted by date and time of the job.
    Filters are applied on all jobs of the logged in user.
    Remaining table information is later added to the context.

    Filters cannot be stacked, only one at a time. Might be a good
    additional feature to be added.

    :param request: Django request object
    :type request: WSGIRequest
    :return: Recent page, context contains recent jobs
    :rtype: HttpResponse
    """
    log_user = request.user
    query = BlastJob.objects.order_by('-date', '-time').filter(user=log_user)
    
    if request.method == "POST":
        title = request.POST.get('filter-title')
        date = request.POST.get('filter-date')
        min_len = request.POST.get('filter-min-length')
        max_len = request.POST.get('filter-max-length')

        # Filter on title, date, min query length, max query length
        # Will always get the 10 most recent results
        
        if min_len or max_len:
            query = query.annotate(sequence_length=Length('sequence'))

        if title:
            query = query.filter(title__icontains=title)
        if date:
            query = query.filter(date=date)
        if min_len:
            query = query.filter(sequence_length__gte=min_len)
        if max_len:
            query = query.filter(sequence_length__lte=max_len)
        
        filters_active = any([title, date, min_len, max_len])
        if not filters_active:
            query = query[:10]
    else:
        query = query[:10]
    user_jobs = query

    # Get the remaining table information
    for job in user_jobs:
        job.hits = job.blasthit_set.all().count()
        job.query_length = len(job.sequence)
    
    context = {
        'recent_jobs': user_jobs
    }
    return render(request, 'pages/recent.html', context)
