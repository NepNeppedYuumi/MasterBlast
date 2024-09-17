# Third-party imports
import pytest

# Local imports
from Blaster.models import BlastJob, UnprocessedBlastJob
from testing import create_request, create_blast_job


@pytest.mark.django_db
def test_unprocessed_blast_job_creation(
        create_request: pytest.fixture, create_blast_job: pytest.fixture):
    """
    Tests if a `BlastJob` automatically creates an
    `UnprocessedBlastJob` referencing the `BlastJob`
    when it has been created.
    :param create_request: A fixture to create a request
    :type create_request: pytest.fixture
    :param create_blast_job: A fixture to create a blast job
    :type create_blast_job: pytest.fixture
    """
    request = create_request()
    job = BlastJob.objects.create_blast_job(request, "", "", "", "")
    assert UnprocessedBlastJob.check_blast_job_is_processed(job.pk) is False


@pytest.mark.django_db
def test_unprocessed_blast_job_deletion(
        create_request: pytest.fixture, create_blast_job: pytest.fixture):
    """Creates an `UnprocessedBlastJob` through `BlastJob`.

    It creates an `UnprocessedBlastJob` and then tests if it's possible
    to delete said `UnprocessedBlastJob` successfully through the
    method available for this.
    
    :param create_request: A fixture to create a request:
    :type create_request: pytest.fixture
    :param create_blast_job: A fixture to create a blast job
    :type create_blast_job: pytest.fixture
    """
    request = create_request()
    job = BlastJob.objects.create_blast_job(request, "", "", "", "")
    assert UnprocessedBlastJob.check_blast_job_is_processed(job.pk) is False
    UnprocessedBlastJob.remove_by_blast_job(job.pk)
    assert UnprocessedBlastJob.check_blast_job_is_processed(job.pk) is True
