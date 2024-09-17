# Third-party imports
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import register

# Local imports
from Blaster.models import SharedJobs
from Blaster.utils.queries import get_blast_job_from_id, \
    get_blast_hits_from_job_id


def blast_result_page(request: WSGIRequest, blast_job_id: int) -> HttpResponse:
    """Renders the BLAST result page.

    Takes a BlastJob id and renders it with its hits in a page.
    On POST, all selected hits are retrieved from the page,
    and rendered om the comparison page.

    :param request: Django request object
    :type request: WSGIRequest
    :param blast_job_id: id for the BLAST job to be shown on page
    :type blast_job_id: int
    :return: blast_results page
    :rtype: HttpResponse
    """
    # Take selected hits to comparison on POST
    if request.method == 'POST':
        selected_hits = request.POST.getlist('selected_hits')
        request.session['selected_hits'] = selected_hits
        return redirect('comparison')
    
    # Render 404 if job can't be retrieved
    try:
        job = get_blast_job_from_id(blast_job_id)
    except (Http404, ValueError):
        return render(request, '404.html', status=404)
    
    # Calculate user permission
    job_buddies = job.user.blastbuddies_as_user.buddie.all()
    shared_already_rev = {}
    for buddie in job_buddies:
        shared_jobs = SharedJobs.objects.filter(user = buddie).first()
        shared_already_rev[buddie.id] = shared_jobs.shared_job.filter(
            id = blast_job_id).exists() if shared_jobs else False
    job_is_shared = shared_already_rev.get(request.user.id, False)

    # Render 403 if user has no permission
    if (job.user is not None and job.user != request.user) and (
        job.user is not None and not job_is_shared):
            return render(request, '403.html')

    # Calculate jobs that have been shared already
    hits = get_blast_hits_from_job_id(blast_job_id)
    user_buddies = request.user.blastbuddies_as_user.buddie.all()
    shared_already = {}
    for buddie in user_buddies:
        shared_jobs = SharedJobs.objects.filter(user = buddie).first()
        shared_already[buddie.id] = shared_jobs.shared_job.filter(
            id = blast_job_id).exists() if shared_jobs else False

    context = {
        'job': job,
        'hits': hits,
        'shared_already': shared_already
    }
    return render(request, "pages/blast_results.html", context)


def share_to_buddie(request, job_id: int, buddie_username: str) -> HttpResponseRedirect:
    """shares job to selected buddie.

    Takes the Job id from active blast result page and shares it
    with the selected buddie. If the buddie has no sharedjobs table jet
    then one will be made to prevent an error. After adding the 
    sharedjob it redirects back to the same blast job page to reload 
    the list of blast buddies to share with if the job was already shared with

    :param request: Django request object
    :type request: WSGIRequest
    :param job_id: id for the BLAST job to be shared
    :type job_id: int
    :param buddie_username: username of the buddy to share with
    :type buddie_username: str
    :return: redirect back to the same result page
    :rtype: redirect
    """
    name_id_obj = get_object_or_404(User, username = buddie_username)

    shared_job_instance, created = SharedJobs.objects.get_or_create(
        user = name_id_obj)
    shared_job_instance.shared_job.add(job_id)

    return redirect("/blast_result/" + str(job_id))


@register.filter
def get_item_from_dic(dictionary, key): 
    """function to get a item from a dict

    Takes a dictonary and then returns the values of a given key.
    Designed to be used to get the status of the buddies if the job 
    has allready been shared.

    ---
    RESTRUCTURING NOTICE

    This function should be moved to the templatetags module.
    ---

    :param dictionary: a dict with the ids of all the 
    buddies of the user, and a bool for the status
    :type dictionary: dict{int: bool}
    :param key: int for the id of the user buddie to check in 
    dictionary
    type key: int 
    :return: return the key from the dictionary wich  
    :rtype: bool
    """
    return dictionary.get(key)
