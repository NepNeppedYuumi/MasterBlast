# Third-party imports
import pytest

# Local imports
from Blaster.models import BlastJob, BlastHit
from testing import (create_request, create_blast_job, create_accession,
                     create_hit)


@pytest.mark.parametrize(
    "identities, align_length, expected_percentage",
    [
        (0, 100, 0.0),
        (32, 67, 47.76),
        (4500, 150043, 3.0),

        # it is currently observed that it can exceed 100.
        (167, 145, 115.17),
    ],
)
@pytest.mark.django_db
def test_blast_hit_percentage_identity(
        create_hit: pytest.fixture, identities: int, align_length:
        int, expected_percentage: int):
    """
    Tests if the percentage identity of a hit is properly
    calculated.

    Uses the `create_hit` fixture, to only need to use
    the relavant variabels.
    
    It is parametrized that different identities and alignment lengths
    are properly used to calculate the expected result.

    On testing, it was observed that the implementation could exceed
    100, so this is currently included in the test.

    :param create_hit: pytest fixture to create a hit.
    :type create_hit: pytest.fixture
    :param identities: The number of identities.
    :type identities: int
    :param align_length: The alignment length.
    :type align_length: int
    :param expected_percentage: The expected percentage identity.
    :type expected_percentage: float
    """
    hit = create_hit(identities=identities, align_length=align_length)
    assert hit.percentage_identity == expected_percentage


@pytest.mark.parametrize(
    "query_end, query_start, query_length, expected_coverage",
    [
        # situations that shouldn't happen
        (0, 0, 14, 7.14),

        # intended behaviour
        (40, 1, 600, 6.67),
        (40, 1, 60, 66.67),
        (75, 3, 80, 91.25),

        # it is currently expected that it can exceed 100.
        (75, 3, 70, 104.29),
    ],
)
@pytest.mark.django_db
def test_blast_hit_query_coverage(
        create_hit: pytest.fixture, query_end: int, query_start: int,
        query_length: int, expected_coverage: int):
    """
    Tests if the query coverage of a hit is properly
    calculated.

    Uses the `create_hit` fixture, to only need to use
    the relavant variabels.

    It is parametrized to test multiple cases:
        It tests the result of a situation that shouldn't happen.
        The intended behaviour,
        And that the calculation can currently exceed 100.
    The extra situations are added to ensure expectations 
    of what the calculation currently does.

    :param create_hit: The function to create a hit.
    :type create_hit: pytest.fixture
    :param query_end: The query end position.
    :type query_end: int
    :param query_start: The query start position.
    :type query_start: int
    :param query_length: The query length.
    :type query_length: int
    :param expected_coverage: The expected query coverage.
    :type expected_coverage: float
    """
    hit = create_hit(query_end=query_end, query_start=query_start,
                     query_length=query_length)
    assert hit.query_coverage == expected_coverage
