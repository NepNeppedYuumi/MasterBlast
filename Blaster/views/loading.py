# Third-party imports
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

# Local imports
from Blaster.views.blast_results import blast_result_page
from Blaster.models import UnprocessedBlastJob


def loading_result_page(request: WSGIRequest, job_id: int) \
        -> HttpResponse | HttpResponseRedirect:
    """
    The loading result page will check if the job has been processed.
    If the job has been processed, a redirection to the result page
    will be returned.
    If the job has not been processed, the loading page will be
    rendered.

    :param request: The request object.
    :type request: WSGIRequest
    :param job_id: the id of the job that that is to be loaded.
    :type job_id: int
    :return: HttpResponse or HttpResponseRedirect.
    :rtype : HttpResponse | HttpResponseRedirect
    """
    if UnprocessedBlastJob.check_blast_job_is_processed(job_id):
        return redirect(reverse(blast_result_page, args=[job_id]))

    title = UnprocessedBlastJob.objects.filter(job__pk=job_id).first().job.title

    return render(request, "pages/loading_result.html", context={"title": title})


def get_processed_status(request: WSGIRequest, job_id: int) -> JsonResponse:
    """
    This function is used for the client to retrieve if a job has
    been processed yet.
    It returns a JsonResponse with a boolean value of the
    status.
    
    status:
        True = the job has been processed
        False = the job has not been processed yet.

    :param request: The request object.
    :type request: WSGIRequest
    :param job_id: The job id.
    :type job_id: int
    :return: JsonResponse containing the status.
    :rtype: bool
    """
    try:
        status = UnprocessedBlastJob.check_blast_job_is_processed(job_id)
    except ValueError:
        status = False
    return JsonResponse({"status": status})