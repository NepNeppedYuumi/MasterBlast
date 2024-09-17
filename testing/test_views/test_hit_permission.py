# Third-party imports
from django.test import Client
import pytest

# Local imports
from Blaster.models import BlastHit
from testing import (create_hit, create_blast_job, create_request,
                     create_accession)


@pytest.mark.django_db
def test_hit_view_404():
    """
    Tests if the hit view will properly return a 404 if the hit
    does not exist.

    Limitation:
        Through the absence of other tests testing
        the hit view, it can not be proven if this tests is
        properly testing the correct thing.
    """
    client = Client()

    response = client.get("/blast_hit/1")

    assert '404.html' in [template.name for template in response.templates]
