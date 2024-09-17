# Third-party imports
from celery import shared_task

# Local imports
from Blaster.models import BlastJob
from Blaster.utils.ncbi import perform_blast_job


# --- test purposes ---
"""
Example Celery tasks.

These function serves as an example of how a Celery shared task could be created.

Note: These functions are not used in the project and are provided solely for demonstration purposes.
    It can be considered to remove or move them.
"""
@shared_task
def add(x, y):
    return x + y


@shared_task()
def database_write():
    job = BlastJob.objects.create(
        program = "blastn",
        sequence = "atatatatatatatatatatatatatatatatatatatatat",
        title="attempt for celery"
    )

    job.save()


# --- used tasks ---
"""
Celery tasks used in the project.

Note: This section of documentation can be removed if 
    the demonstrative tasks are moved or removed.
"""
@shared_task
def perform_blast_job_task(*args, **kwargs) -> None:
    """A wrapper function for `perform_blast_job`.

    This allows for a blast job to be run as a task,
    while still being usable without tasks.

    It has been done like this for the task to be registered
    within tasks.py and the namespace to be clear.

    :rtype: None
    """
    return perform_blast_job(*args, **kwargs)
