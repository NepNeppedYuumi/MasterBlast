# Third-party imports
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from kombu.exceptions import OperationalError

# Local imports
from Blaster.forms.index_form import (validate_index_form, read_index_file,
                                      IndexValidationEnum, process_index_form)
from Blaster.models import BlastJob
from Blaster.tasks import perform_blast_job_task
from Blaster.utils.ncbi import perform_blast_job
from Blaster.views.loading import loading_result_page


def index_page(request: WSGIRequest) -> HttpResponse | HttpResponseRedirect:
    """
    Renders the index page.

    The index page contains a form which provides the ability to
    blast to the NCBI database.

    Currently possible are:
        Use BLASTn and BLASTp.
        Provide a name for the blastjob.
        Input a sequence through text or through a file.

    If the form has been filled in the data from the form
    is processed and validated.
        If a file is provided the contents of the files 
        are parsed to a string.
    More information on processing and validation can be found
    in forms/index_form.py

    It is required for a valid sequence to be present to blast.
    If an invalid sequence is provided the page will be refreshed
    and a relevant error message will show up.
    
    When a valid sequence is provided the sequence and other relevant 
    information will be stored in the database.
    The job will then be executed against the NCBI database.

    It is intended for the blast to be performmed asynchronously
    through the use of celery.
    If it's not possible to communicate with celery, the job
    will still be performed, but synchronously instead.

    If all performs as normal, one will referred to the loading
    page while the job is processing.
    If the job is performed synchronously it will look as if
    the webpage is lagging.
        For this reason it is recommended to deprecate this
        behaviour when deploying, and wait with processing
        user's jobs instead.

    :param request: The request object.
    :type request: WSGIRequest
    :return: HttpResponse or HttpResponseRedirect.
    :rtype HttpResponse or HttpResponseRedirect
    """

    if request.method == "POST":
        blast_mode = request.POST.get("blast-mode")
        job_name = request.POST.get("job-name")
        seq_text = request.POST.get("seq-text")
        seq_file = request.FILES.get("seq-file")
        seq_file_text = read_index_file(seq_file)

        validation = validate_index_form(
            blast_mode, job_name, seq_text, seq_file, seq_file_text)

        if validation != IndexValidationEnum.VALID:
            messages.error(request, f"Error: {validation.name}")

            return redirect(index_page)

        header, sequence = process_index_form(
            seq_text, seq_file, seq_file_text
        )

        blast_job: BlastJob = BlastJob.objects.create_blast_job(
            request, job_name, blast_mode, header, sequence
        )

        try:
            perform_blast_job_task.delay(blast_job.id)
        except OperationalError:
            # In case it's not possible to communicate with Celery
            perform_blast_job(blast_job.id)

        return redirect(reverse(loading_result_page, args=[blast_job.id]))
    return render(request, "pages/index.html")
