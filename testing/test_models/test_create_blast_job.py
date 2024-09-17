# Standard library imports
import re
from enum import Enum, auto

# Third-party imports
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
import pytest
from testing import create_request

# Local imports
from Blaster.models.BlastJob import BlastJob


class TitleTestEnum(Enum):
    """
    Holds options for the possible ways the title
    for `test_BlastJob_title` can be generated.
    Is used to make the parameters clearer for the tests.
    """
    FROM_TITLE = auto()
    FROM_HEADER = auto()
    RANDOM_MASTERBLAST = auto()


@pytest.mark.parametrize(
    "title, program, header, sequence, expected",
    [
        ("", "", "", "", TitleTestEnum.RANDOM_MASTERBLAST),
        ("a", "", "", "", TitleTestEnum.FROM_TITLE),
        ("a" * 100, "", "", "", TitleTestEnum.FROM_TITLE),

        ("", "", "a", "", TitleTestEnum.FROM_HEADER),
        ("", "", "a" * 100, "", TitleTestEnum.FROM_HEADER),
        ("", "", "a a", "", TitleTestEnum.FROM_HEADER),
        ("", "", "a" * 100 + " " + "a" * 100, "", TitleTestEnum.FROM_HEADER),

        ("a", "", "a", "", TitleTestEnum.FROM_TITLE),
    ]
)
@pytest.mark.django_db
def test_blast_job_title(
        create_request: pytest.fixture, title: str, program: str,
        header: str, sequence: str, expected: TitleTestEnum):
    """
    It is parametrized to test multiple options using the same inputs.

    Tests if the input variables `title` and `header` are processed
    properly to generate a title.
    There are three possible results for a title:
     - The variable `title` becomes the title
     - The variable `header` is used to generate the title
     - The title becomes "MasterBlast" followed by numbers.

    The logic of the create_blast_job should follow the steps from top
    to bottom, and it will go to the next step if the variable used
    is an empty string.

    It's tested if this is done correctly using regex, to see
    if the title matches the expected pattern.
    The variables used to create the pattern are the same variables
    used to create the tite.

    :param create_request: The function to create a request.
    :type create_request: pytest.fixture
    :param title: The job title.
    :type title: str
    :param program: The program name.
    :type program: str
    :param header: The header.
    :type header: str
    :param sequence: The sequence.
    :type sequence: str
    :param expected: The expected result.
    :type expected: TitleTestEnum
    """
    job = BlastJob.objects.create_blast_job(create_request(), title,
                                            program, header, sequence)

    match expected:
        case TitleTestEnum.FROM_TITLE:
            pattern = rf"^{title}$"
        case TitleTestEnum.FROM_HEADER:
            pattern = rf"^{header.split(' ')[0]}$"
        case TitleTestEnum.RANDOM_MASTERBLAST:
            pattern = r"^MasterBlast[0-9]*$"
        case _:
            raise UserWarning

    assert re.match(pattern, job.title) is not None


@pytest.mark.parametrize(
    "user_presence, title, program, header, sequence, "
    "expectation",
    [
        (True, "", "", "", "", True),
        (False, "", "", "", "", False),
    ],
)
@pytest.mark.django_db
def test_blast_job_user_assignment(
        create_request: pytest.fixture, user_presence: bool, title: str,
        program: str, header: str, sequence: str, expectation: bool):
    """
    Tests if the user id will be properly applied.
    If there is a user, the user id should become the user id
    of the blastjob.
    If there is no user, the user of the blastjob should be None

    Limitation:
        Through the usage of create_request fixture in a 
        parametrized test, it should currently not be possible to 
        test multiple users, as it's not possible to create users with 
        duplicate usernames.

    :param create_request: A fixture to create a request
    :type create_request: pytest.fixture
    :param user_presence: Wether or not a user should be present
    :type user_presence: bool
    :param title: The title of the job
    :type title: str
    :param program: The program of the job
    :type program: str
    :param header: The header of the job
    :type header: str
    :param sequence: The sequence of the job
    :type sequence: str
    :param expectation: The expected result
    :type expectation: bool
    """
    request = create_request(user_presence)
    job = BlastJob.objects.create_blast_job(request , title, program,
                                            header, sequence)

    if expectation is True:
        assert job.user_id == request.user.id
    else:
        assert job.user_id is None


