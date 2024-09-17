# Third-party imports
from django.db.models.query import QuerySet
from django.http import Http404

# Local imports
from Blaster.models import BlastJob, EntrezAccession, BlastHit, \
    UnprocessedBlastJob


"""
    REORGANIZATION NOTICE
    
    The query functions within this file should be moved to 
    the Blaster/models module, and should become methods 
    of their respective model, or model manager.

    No more functions should be added to this file, nor should
    more queries be added to the Blaster/utils module.
"""


def get_blast_job_from_id(id: int) -> BlastJob | None:
    """Returns a BlastJob retrieved by id or raises an error.

    :param id: identifier for the BlastJob to be returned.
    :type id: int.
    :raises Http404: if the BlastJob does not exist.
    :raises ValueError: if multiples BlastJobs are found with the id.
    :return: object that stores information about the BLAST job.
    :rtype: BlastJob or None.
    """
    try:
        return BlastJob.objects.get(id=id)
    except BlastJob.DoesNotExist:
        raise Http404('Error: BLAST hit with the specified ID does not exist')
    except:
        raise ValueError(
            'Error: Something went wrong while trying to fetch the BLAST job')


def get_entrez_accession_from_code(code: str) -> EntrezAccession | None:
    """Returns EntrezAccession retrieved by code or raises an error.

    :param code: identifier for the EntrezAccession to be returned.
    :type code: str.
    :raises EntrezAccession.DoesNotExist: if the object does not exist.
    :raises ValueError: if multiple EntrezAccession objects are found.
    :return: object that stores information about an Entrez accession
             entry.
    :rtype: EntrezAccession or None.
    """
    try:
        return EntrezAccession.objects.get(code=code)
    except EntrezAccession.DoesNotExist:
        raise EntrezAccession.DoesNotExist(
            'Error: Entrez accession with the specified code does not exist')
    except:
        raise ValueError(
            'Error: Something went wrong while\
                  trying to fetch the Entrez accession')


def get_blast_hit_from_id(id: int) -> BlastHit:
    """Returns a BlastHit with the given id or raises an error.

    :param id: identifier for the BlastHit to be returned.
    :type id: int..
    :raises Http404: if the object does not exist.
    :raises ValueError: if multiple objects with the id are found.
    :return: object that stores information about the BLAST hit.
    :rtype: BlastHit.
    """
    try:
        return BlastHit.objects.get(id=id)
    except BlastHit.DoesNotExist:
        raise Http404('Error: BLAST hit with the specified ID does not exist')
    except:
        raise ValueError(
            'Error: Something went wrong while trying to fetch the BLAST hit')


def get_blast_hits_from_job_id(id: int) -> QuerySet[BlastHit]:
    """Returns BlastHit objects related to a job with a specific id.

    :param id: identifier for the BlastJob to return the hits of.
    :type id: int.
    :return: set of objects that store information about a BLAST hit.
    :rtype: QuerySet[BlastHit]
    """
    return BlastHit.objects.filter(job__id=id)


def check_blast_job_is_processed(id: int) -> bool:
    """Returns whether a BlastJob is processed as a boolean.

    :param id: identifier for the UnprocessedBlastJob to be checked.
    :type id: int.
    :return: True if a BLAST job is processed, False if unprocessed.
    :rtype: bool.
    """
    return not UnprocessedBlastJob.objects.filter(job__id=id).exists()
