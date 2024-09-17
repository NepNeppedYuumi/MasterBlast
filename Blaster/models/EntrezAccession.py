# Standard library imports
from typing import Union

# Third-party imports
from django.core.exceptions import ValidationError
from django.db import models

# Local imports
from .EntrezAccessionCache import EntrezAccessionCache


class EntrezAccessionManager(models.Manager):
    def create_entrez_accession(self,
            code: str,
            organism: str
    ) -> Union["EntrezAccession", str]:
        """Creates and returns an EntrezAccession object

        Tries to create an EntrezAccession object and return it. If
        a ValidationError occurs, returns an error message as a string. 

        :return: The created EntrezAccession object or an error message
        :rtype: EntrezAccession | str
        """
        try:
            accession = self.create(
                code=code,
                organism=organism
            )
            accession.save()
            return accession
        except ValidationError:
            return 'Error: ValidationError occurred while creating EntrezAccession'


class EntrezAccession(models.Model):
    """Stores information related to an EntrezAccession accession code

    For every accession code associated with a BlastHit object, an
    EntrezAccession object is created. The code is always linked to an
    organism, and a field for a relation to an EntrezAccessionCache,
    for storing GenBank and FASTA data, is filled upon visiting the
    BLAST hit page.
    """
    objects = EntrezAccessionManager()

    code = models.CharField(
        max_length=25,
        blank=False,
        null=False
    )
    organism = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    cache = models.OneToOneField(
        EntrezAccessionCache,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )