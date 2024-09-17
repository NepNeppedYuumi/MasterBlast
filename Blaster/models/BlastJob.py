# Third-party imports
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.contrib.auth.models import User

# Local imports
from .UnprocessedBlastJob import UnprocessedBlastJob


class BlastJobManager(models.Manager):
    def create_blast_job(self, request: WSGIRequest, title: str, program: str, 
                         header: str, sequence: str) -> "BlastJob":
        """Creates a BlastJob object.

        Creates a BlastJob instance with the provided parameters and
        also creates an UnprocessedBlastJob instance linked to it.
        If there is a title given, it will be used as the title.
        If there is a header, it will always be stored. If there is no
        title, but there is a header, the header will be used as the
        title. If there is no title or header, "MasterBlast[job_id]"
        will be used.

        :return: The created BlastJob object
        :rtype: BlastJob
        """
        job = self.create(
            program=program,
            sequence=sequence
        )

        if title:
            job.title = title
        if header:
            job.header = header
            if not title:
                job.title = header.split(' ')[0]
        if not title and not header:
            job.title = f'MasterBlast{job.id}'

        if request.user.is_authenticated:
            job.user = request.user
        job.save()

        UnprocessedBlastJob.objects.create(
            job=job
        )

        return job


class BlastJob(models.Model):
    """A BLAST query run in MasterBlast
    
    The BlastJob model represents a single query run in MasterBlast.
    The relation to a User object and the error_msg and header fields are
    optional. All of the other fields are always filled upon creation
    of a BlastJob.
    """
    objects = BlastJobManager()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    title = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )
    program = models.CharField(
        max_length=6,
        blank=False,
        null=False
    )
    header = models.TextField(
        blank=False,
        null=False
    )
    sequence = models.TextField(
        blank=False,
        null=False
    )
    date = models.DateField(
        auto_now_add=True,
        blank=False,
        null=False
    )
    time = models.TimeField(
        auto_now_add=True,
        blank=False,
        null=False
    )
    error_msg = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
