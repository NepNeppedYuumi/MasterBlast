# Standard library imports
from typing import Union

# Third-party imports
from django.db import models
from django.core.exceptions import ValidationError

# Local imports
from .BlastJob import BlastJob
from .EntrezAccession import EntrezAccession


class BlastHitManager(models.Manager):
    def create_hit(self,
                   blast_job_id: int,
                   accession_id: int,
                   description: str,
                   blast_score: int,
                   bit_score: float,
                   e_value: float,
                   identities: int,
                   align_length: int,
                   query_start: int,
                   query_end: int,
                   query_length: int,
                   subject_seq: str,
                   subject_start: int,
                   subject_end: int
                   ) -> Union["BlastHit", str]:
        """Creates a BlastHit object.

        Creates a BlastHit instance with the provided parameters and
        calculates percentage_identity and query_coverage before
        saving. If any errors occur during creation, an error message
        is returned as a string.

        :return: The created BlastHit object or an error message
        :rtype: BlastHit | str
        """
        try:
            percentage_identity = round(
                (identities / align_length) * 100, 2)
            query_coverage = round(
                (query_end - query_start + 1) / query_length * 100, 2)

            return self.create(
                job_id=blast_job_id,
                accession_id=accession_id,
                description=description,
                blast_score=blast_score,
                bit_score=bit_score,
                e_value=e_value,
                identities=identities,
                percentage_identity=percentage_identity,
                align_length=align_length,
                query_start=query_start,
                query_end=query_end,
                query_coverage=query_coverage,
                subject_seq=subject_seq,
                subject_start=subject_start,
                subject_end=subject_end
            )
        except ValidationError:
            return 'Error: a ValidationError occurred while creating BlastHit'
        except ValueError:
            return 'Error: a Value error occurred'


class BlastHit(models.Model):
    """A single hit found in a BLAST query.

    The BlastHit model represents a single BLAST hit and is always
    linked to a BlastJob on creation. All of the fields are filled upon
    creation.
    """
    objects = BlastHitManager()

    job = models.ForeignKey(
        BlastJob,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    accession = models.ForeignKey(
        EntrezAccession,
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    description = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )
    blast_score = models.PositiveIntegerField(
        blank=False,
        null=False
    )
    bit_score = models.FloatField(
        blank=False,
        null=False
    )
    e_value = models.FloatField(
        blank=False,
        null=False
    )
    identities = models.PositiveIntegerField(
        blank=False,
        null=False
    )
    percentage_identity = models.FloatField(
        blank=False,
        null=False
    )
    align_length = models.PositiveIntegerField(
        blank=False,
        null=False
    )
    query_start = models.PositiveIntegerField(
        blank=False,
        null=False
    )
    query_end = models.PositiveIntegerField(
        blank=False,
        null=False
    )
    query_coverage = models.FloatField(
        blank=False,
        null=False
    )
    subject_seq = models.TextField(
        blank=False,
        null=False
    )
    subject_start = models.PositiveIntegerField(
        blank=False,
        null=False
    )
    subject_end = models.PositiveIntegerField(
        blank=False,
        null=False
    )
