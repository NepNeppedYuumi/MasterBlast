# Third-party imports
from django.db import models
from django.contrib.auth.models import User

# Local imports
from Blaster.models.BlastJob import BlastJob


class SharedJobs(models.Model):
    """BlastJob objects shared with a user
    
    Allows a user to store BLAST jobs that have been shared with them
    by other users of MasterBlast.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="shared_jobs_user"
    )
    shared_job = models.ManyToManyField(
        BlastJob,
        related_name="shared_job"
    )
