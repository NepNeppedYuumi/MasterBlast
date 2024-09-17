# Third-party imports
from django.db import models
from django.contrib.auth.models import User


class BlastBuddies(models.Model):
    """A user's list of MasterBlast friends
    
    BlastBuddies are used to allow users to share jobs with each other.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='blastbuddies_as_user'
    )
    buddie = models.ManyToManyField(
        User,
        related_name="blastbuddies_as_buddie"
    )
