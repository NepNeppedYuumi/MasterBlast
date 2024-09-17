# Third-party imports
from django.http import Http404
import pytest

# Local imports
from Blaster.utils.queries import get_blast_job_from_id
from Blaster.utils.queries import get_entrez_accession_from_code
from Blaster.utils.queries import get_blast_hit_from_id
from Blaster.utils.queries import get_blast_hits_from_job_id
from Blaster.utils.queries import check_blast_job_is_processed
from Blaster.models import BlastHit, BlastJob, \
    EntrezAccession, UnprocessedBlastJob


"""
REFACTORING NOTICE

All functionality within this file is part of database related events.
As such it should be moved to testing/test_models

A refactoring notice has been added to test_queries.py informing the
functionality should be moved to the models module as well. 
"""

# Test cases for the get_blast_job_from_id function
@pytest.mark.parametrize(
    "setup_info, expected_exception,\
          expected_message, test_id",
    [
        # Test validity with a valid job
        (
            {"id": 1, "title": "valid-job1"}, None, None, 1
        ),
        # Test validity with a negative job id
        (
            {"id": -1, "title": "valid-job7"}, None, None, -1
        ),
        # Test a job of which the id is created as a string
        (
            {"id": "2", "title": "valid-job2"}, None, None, 2
        ),


        # Test exception with a job id that does not exist
        (
            None, Http404,
          'Error: BLAST hit with the specified ID does not exist',
            1
        ),
        # Test exception with a job id that is negative
        (
            None, Http404,
          'Error: BLAST hit with the specified ID does not exist',
            -1
        ),
        # Test exception with None as job id
        (
            None, Http404, 
            "Error: BLAST hit with the specified ID does not exist",
            None
        ),
        # Test exception with an id that is a string
        (
            None, Http404,
            'Error: BLAST hit with the specified ID does not exist',
            "1"
        ),


        # Test exception with an non-integer id
        (
            None, ValueError,
          'Error: Something went wrong while trying to fetch the BLAST job',
            "one"
        ),
        # Test exception with special characters as id
        (
            None, ValueError,
          'Error: Something went wrong while trying to fetch the BLAST job',
            "!@#$%"
        ),
        # test exception with a list as job id
        (
            None, ValueError,
          'Error: Something went wrong while trying to fetch the BLAST job',
            [1, 2, 3]
        ),
        # Test exception with a dictionary as job id
        (
            None, ValueError,
          'Error: Something went wrong while trying to fetch the BLAST job',
            {"id": 1, "title": 'job'}
        ),
        
    ]
)

@pytest.mark.django_db
def test_get_blast_job_from_id(setup_info: dict | None, 
                               expected_exception: BaseException | None, 
                               expected_message: str | None, 
                               test_id: int | str | list | dict | None,):
    """Test the get_blast_job_from_id function.
    Parametrized to test multiple options using the same inputs.

    Tests:
        - 3 valid job id's
        - 4 job id's that do not exist
        - 4 job id's that are not integers
    
    Wanted to test whether the function can handle very a large id
    value, but the database does not allow this.

    Creates a BlastJob with the given setup_info if provided
    Checks if the expected exception matches the actual exception raised. 
    If no exception is expected, it also checks if the returned BlastJob 
    object has the expected id

    :param setup_info: The setup information for the BlastJob
    :type setup_info: dict | None
    :param expected_exception: Expected exception class
    :type expected_exception: BaseException
    :param expected_message: Expected error message raised
    :type expected_message: str
    :param test_id: id of the BlastJob object to get
    :type test_id: int | str | list | dict | None
    """
    if setup_info:
        BlastJob.objects.create(**setup_info)            
    
    if expected_exception:
        with pytest.raises(expected_exception) as excinfo:
            get_blast_job_from_id(test_id)
        assert str(excinfo.value) == expected_message
    else:
        job = get_blast_job_from_id(test_id)
        assert job.id == test_id


# Test cases for the get_entrez_accession_from_code function
@pytest.mark.parametrize(
    "code, setup_info, expected_exception, expected_message",
    [   
        #Test validity with a normal code
        (
            "valid-code1", 
            {"code": "valid-code1", "organism": "Organism1"}, 
            None, None
        ),
        #Test validity with a very long code
        (
            "a" * 10000, 
            {"code": "a" * 10000, "organism": "Organism3"}, 
            None, None
        ),
        #Test validity with special characters in the code
        (
            "!@#$%^&*()", 
            {"code": "!@#$%^&*()", "organism": "Organism4"}, 
            None, None
        ),
        #Test validity with an empty code
        (
            "", 
            {"code": "", "organism": "Organism5"}, 
            None, None
        ),
        # Test validity with newline in the code
        (
            "new\nline",
            {"code": "new\nline", "organism": "Organism6"},
            None, None
        ),
        # Test validity with a list as code
        (
            '[1, 2, 3]', {"code": "[1, 2, 3]", "organism": "Organism9"},
            None, None
        ),


        #Test exception with a code that does not exist
        (
            "non-existant", None, 
            EntrezAccession.DoesNotExist, 
            "Error: Entrez accession with the specified code does not exist"
        ),
        # Test exception with a code that is negative
        (
            -1, None,
            EntrezAccession.DoesNotExist,
            "Error: Entrez accession with the specified code does not exist"
        ),
        #Test exception with None as code
        (
            None, None, 
            EntrezAccession.DoesNotExist, 
            "Error: Entrez accession with the specified code does not exist"
        ),
        #Test exception the case sensitivity
        (
            "CodeWithCase",
            {"code": "codewithcase", "organism": "Organism7"},
            EntrezAccession.DoesNotExist,
            "Error: Entrez accession with the specified code does not exist"
        ),

    ]
)
@pytest.mark.django_db
def test_get_entrez_accession_from_code(code: str | int | None, 
                                        setup_info: dict | None, 
                                        expected_exception: 
                                        BaseException | None, 
                                        expected_message: str | None):
    """Test the get_entrez_accession_from_code function.
    Parametrized to test multiple options using the same inputs.

    Tests:
        - 6 valid codes
        - 3 codes that do not exist and throw an exception
        - 1 code with case differences that throws an exception
    
    The validity of ValueError is not tested. It can only be triggered by 
    database errors, there was no time left for this. 
        
    Creates a EntrezAccession with the given setup_info if provided
    Checks if the expected exception matches the actual exception raised. 
    If no exception is expected, it also checks if the returned EntreAccession 
    object has the expected code

    :param code: The Entrez accession code
    :type code: str | None
    :param setup_info: Setup information for the Entrez accession.
    :type setup_info: dict | None
    :param expected_exception: Expected exception class.
    :type expected_exception: BaseException | None
    :param expected_message: Expected error message raised
    :type expected_message: str | None
    """
    if setup_info:
        EntrezAccession.objects.create(**setup_info)
    if expected_exception:
        with pytest.raises(expected_exception) as excinfo:
            get_entrez_accession_from_code(code)
        assert str(excinfo.value) == expected_message
    else:
        accession = get_entrez_accession_from_code(code)
        assert accession.code == code


setup_dict = {
    "description": "test_hit",
    "blast_score": 0,
    "bit_score": 0.0,
    "e_value": 0.0,
    "identities": 0,
    "percentage_identity": 0.0,
    "align_length": 0,
    "query_start": 0,
    "query_end": 0,
    "query_coverage": 0,
    "subject_seq": 0,
    "subject_start": 0,
    "subject_end": 0
}

# Test cases for the get_blast_hit_from_id function
@pytest.mark.parametrize(
    "exp_blast_hit_id, setup_info, expected_exception, expected_message",
    [
        # Test with a valid hit
        (1, {"id": 1, **setup_dict}, None, None),
        # Test with a negative hit id
        (-1, {"id": -1,**setup_dict}, None, None),
        # Test a job of which the id is created as a string
        (2, {"id": "2", **setup_dict}, None, None),
        # Test with zero as id
        (0, {"id": 0, **setup_dict}, None, None),

       
        # Test with a hit id that does not exist
        (
            1, None, Http404, 
            "Error: BLAST hit with the specified ID does not exist"
        ),
        # Test with a hit id that is negative
        (
            -1, None, Http404, 
            "Error: BLAST hit with the specified ID does not exist"
        ),
        # Test with None as hit id
        (
            None, None, Http404, 
            "Error: BLAST hit with the specified ID does not exist"
        ),
        # Test with a hit id that is a string
        (
            "1", None, Http404, 
            "Error: BLAST hit with the specified ID does not exist"
        ),
        
        
        # Test with an non-integer id
        (
            "one", None, ValueError, 
            "Error: Something went wrong while trying to fetch the BLAST hit"
        ),
        # Test with special characters as id
        (
            "!@#$%", None, ValueError, 
            "Error: Something went wrong while trying to fetch the BLAST hit"
        ),
        # Test with a list as id
        (
            [1, 2 ,3], None, ValueError, 
            "Error: Something went wrong while trying to fetch the BLAST hit"
        ),
        # Test with a dictionary as id
        (
            {"id": 1, "title": 'hit'}, None, ValueError, 
            "Error: Something went wrong while trying to fetch the BLAST hit"
        ),

    ]
)
@pytest.mark.django_db
def test_get_blast_hit_from_id(exp_blast_hit_id: 
                               int | str | list | dict | None, 
                               setup_info: dict | None, 
                               expected_exception: BaseException | None, 
                               expected_message: str | None):
    """Test the get_blast_hit_from_id function.
    Parametrized to test multiple options using the same inputs.

    Tests:
        - 4 valid hit id's
        - 4 variations of hit id's that do not exist
        - 4 non-integer hit id's that throw an exception

    Creates a BlastHit with the given setup_info if provided
    Checks if the expected exception matches the actual exception raised. 
    If no exception is expected, it also checks if the returned BlastHit 
    object has the expected hit id.

    :param exp_blast_hit_id: Expected blast hit id
    :type exp_blast_hit_id: int | str | list | dict | None
    :param setup_info: Setup information for the blast hit
    :type setup_info: dict | None
    :param expected_exception: Expected exception class
    :type expected_exception: BaseException | None
    :param expected_message: Expected error message raised
    :type expected_message: str | None
    """
    if setup_info:
        job = BlastJob.objects.create() #Create a dummy job
        accession = EntrezAccession.objects.create(code="XYZ", 
                                                   organism="Organism") 
        BlastHit.objects.create(job=job, 
                                accession=accession, 
                                **setup_info)
    if expected_exception:
        with pytest.raises(expected_exception) as excinfo:
            get_blast_hit_from_id(exp_blast_hit_id)
        assert str(excinfo.value) == expected_message
    else:
        hit = get_blast_hit_from_id(exp_blast_hit_id)
        assert hit.id == exp_blast_hit_id



# Test case for successful retrieval of blast hits from a job id
@pytest.mark.django_db
def test_valid_get_blast_hits_from_job_id():
    """Test the get_blast_hits_from_job_id function with valid data.

    Tests if a BlastJob with two BlastHits fetched by the function 
    actually contains the two BlastHits with valid data.
    """
    job = BlastJob.objects.create(title="Valid job")
    accession = EntrezAccession.objects.create(code="XYZ", 
                                               organism="Test Organism")
    BlastHit.objects.create(job=job, accession=accession, **setup_dict)
    BlastHit.objects.create(job=job, accession=accession, **setup_dict)

    hits = get_blast_hits_from_job_id(job.id)

    assert hits.count() == 2
    assert all(hit.job.id == job.id for hit in hits)

# Test case where no blast hits are found for a job id
@pytest.mark.django_db
def test_no_blast_hits_for_job_id():
    """Test the get_blast_hits_from_job_id function with no hits.

    Tests if the function returns an empty QuerySet when no BlastHits
    are found for the given BlastJob
    """
    job = BlastJob.objects.create(title="Valid job")

    hits = get_blast_hits_from_job_id(job.id)

    assert hits.count() == 0

# Test case with a job id that does not exist
@pytest.mark.django_db
def test_invalid_get_blast_hits_from_job_id():
    """Test the get_blast_hits_from_job_id function with an invalid job id.

    Tests if the function returns an empty QuerySet when the given job id
    does not exist in the database.
    """
    
    hits = get_blast_hits_from_job_id(666)

    assert hits.count() == 0


# Test whether a job is processed
@pytest.mark.django_db
def test_check_blast_job_is_processed_false():
    """Test the check_blast_job_is_processed function with an unprocessed job.

    Tests if the function returns False when the given job is unprocessed.
    """
    job = BlastJob.objects.create(title="Unprocessed test job")
    UnprocessedBlastJob.objects.create(job=job)

    processed = check_blast_job_is_processed(job.id)

    assert processed is False

# Test whether a job is not processed
@pytest.mark.django_db
def test_check_blast_job_is_processed_true():
    """Test the check_blast_job_is_processed function with a processed job.

    Tests if the function returns True when the given job is processed.
    """
    job = BlastJob.objects.create(title="Proce test job")

    processed = check_blast_job_is_processed(job.id)

    assert processed is True

# Test whether a non-existing job is processed
@pytest.mark.django_db
def test_check_nonexistent_blast_job():
    """Test the check_blast_job_is_processed function with a non-existing job.

    Verify that a job is considered processed as it doesnt exist
    """
    non_existent_job_id = 666

    is_processed = check_blast_job_is_processed(non_existent_job_id)

    assert is_processed is True