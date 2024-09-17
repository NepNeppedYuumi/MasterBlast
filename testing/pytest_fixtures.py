# Standard library imports
from typing import Callable

# Third-party imports
from django.contrib.auth.models import User, AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory
import pytest

# Local imports
from Blaster.models import EntrezAccession, BlastJob, BlastHit


"""
The fixtures in this file are used to paramaterize tests.
Most of the fixtures function as wrappers.

To use a fixture that uses another fixture, all fixtures used
in the chain are required to have been imported to the other file.
"""


request_factory = RequestFactory()


@pytest.fixture
def create_request() -> Callable:
    """
    Generates a request, with the ability to pass on variables
    which should be assigned.

    Default it will create a request to the home page.

    Default it will create a request with a test user.
    It's possible to generate an AnonymousUser by passing
    False with.

    :rtype Callable
    """

    def create_request_inner(user=True, path="/", method="get") -> WSGIRequest:
        def create_test_user():
            return User.objects.create_user("test_custom_request", "test@test.com", "test")

        if method == "get":
            request = request_factory.get(path)
        else:
            request = request_factory.post(path)

        if user is True:
            request.user = create_test_user()
        else:
            request.user = AnonymousUser()
        return request

    return create_request_inner


@pytest.fixture()
def create_blast_job():
    """
    A wrapper for the creation of a blast job with custom variables.

    Defaults to empty strings.
    Requires a WSGIRequest to be passed on explicitly to work.
    :rtype Callable
    """
    def create_blast_job_inner(
            request: WSGIRequest, title="", program="", header="", sequence=""
    ):
        return BlastJob.objects.create_blast_job(
            request, title, program, header, sequence
        )

    return create_blast_job_inner


@pytest.fixture()
def create_accession():
    """
    A wrapper for the creation of an accession with custom variables.

    Defaults to empty strings.
    :rtype Callable
    """
    def create_accession_inner(code="", organism=""):
        return EntrezAccession.objects.create_entrez_accession(code, organism)

    return create_accession_inner


@pytest.fixture()
def create_hit(create_request, create_blast_job, create_accession):
    """
    A wrapper for the creation of a hit.

    Automatically creates a request, job and accession
    for ease of usage.

    The fixture can be used to only actively initialize a selection
    of the hit variables.

    :param create_request: A pytest fixture that allows creating
        a request
    :param create_blast_job: A pytest fixture that allows
        creating a blast job
    :param create_accession: A pytest fixture that allows
        creating an accession
    :rtype Callable`
    """
    request = create_request(False)
    job = BlastJob.objects.create_blast_job(request, "", "", "", "")
    acc = create_accession()

    def create_hit_inner(blast_job_id: int = job.pk,
                         accession_id: int = acc.pk,
                         description: str = "",
                         blast_score: int = 0,
                         bit_score: float = 0.0,
                         e_value: float = 0.0,
                         identities: int = 0,
                         align_length: int = 1,
                         query_start: int = 0,
                         query_end: int = 0,
                         query_length: int = 1,
                         subject_seq: str = "",
                         subject_start: int = 0,
                         subject_end: int = 0):
        return BlastHit.objects.create_hit(
            blast_job_id=blast_job_id,
            accession_id=accession_id,
            description=description,
            blast_score=blast_score,
            bit_score=bit_score,
            e_value=e_value,
            identities=identities,
            align_length=align_length,
            query_start=query_start,
            query_end=query_end,
            query_length=query_length,
            subject_seq=subject_seq,
            subject_start=subject_start,
            subject_end=subject_end
        )

    return create_hit_inner
