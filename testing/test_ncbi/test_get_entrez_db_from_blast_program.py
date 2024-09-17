# Third-party imports
import pytest

# Local imports
from Blaster.utils.ncbi import get_entrez_db_from_blast_program


@pytest.mark.parametrize(
    "valid_program, expected_db", 
    [
        ('blastn', 'nucleotide'),
        ('blastp', 'protein'),
    ]
)
def test_valid_programs(valid_program: str, expected_db: str) -> None:
    """Tests valid cases for get_entrez_db_from_blast_program.

    The function should only return a database in string format if the
    program is either blastn or blastp. Otherwise, the function would
    raise a ValueError.

    :param valid_program: the BLAST program
    :type valid_program: str
    :param expected_db: the expected database returned
    :type expected_db: str
    """
    assert get_entrez_db_from_blast_program(valid_program) == expected_db


@pytest.mark.parametrize(
    "program", 
    [
        ('BLASTN'), # Case insensitivity
        ('BLASTP'), # Case insensitivity
        ('blastn '), # Leading/trailing whitespace
        (' blastn'), # Leading/trailing whitespace
        (' blastn '), # Leading/trailing whitespace
        ('bLaStN'), # Random capitalization
        ('BlastN'), # Random capitalization
        ('   blastn   '), # Whitespace within input
        ('blastx'), # Unsupported program
        ('tblastn'), # Unsupported program
        ('tblastx'), # Unsupported program
        ('psiblast'), # Unsupported program
        ('rpsblast'), # Unsupported program
        ('rpstblastn'), # Unsupported program
        (''), # Empty string
        (1), # Type protection
        (None), # None
    ]
)
def test_invalid_programs(program: str | int | None) -> None:
    """Tests invalid cases for get_entrez_db_from_blast_program.

    The tested function will raise a ValueError if the input program is
    not blastn or blastp. Different strings similar to valid cases and
    other types of invalid inputs are tested.

    :param program: the BLAST program
    :type program: str
    """
    with pytest.raises(ValueError):
        get_entrez_db_from_blast_program(program)
