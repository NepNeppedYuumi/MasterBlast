# Third-party imports
from django.db import models


class EntrezAccessionCacheManager(models.Manager):
    def create_entrez_accession_cache(self,
            genbank: str=None,
            fasta: str=None
            ) -> "EntrezAccessionCache":
        """Creates an EntrezAccessionCache object

        If no parameters are passed, defaults to empty strings.

        :param genbank: GenBank file content, defaults to None
        :type genbank: str, optional
        :param fasta: FASTA file content, defaults to None
        :type fasta: str, optional
        :return: the created EntrezAccessionCache object
        :rtype: EntrezAccessionCache
        """
        return self.create(
            genbank=genbank if genbank else '',
            fasta=fasta if fasta else ''
            )


class EntrezAccessionCache(models.Model):
    """Cache for GenBank and FASTA data for an EntrezAccession
    
    This cache is only filled when a user visits the BLAST hit page.
    It's possible that the GenBank or FASTA files can't be fetched, so
    the fields can be empty.
    """
    objects = EntrezAccessionCacheManager()

    date = models.DateField(
        auto_now=True,
        blank=False,
        null=False
    )
    genbank = models.TextField(
        blank=True,
        null=True
    )
    fasta = models.TextField(
        blank=True,
        null=True
    )
