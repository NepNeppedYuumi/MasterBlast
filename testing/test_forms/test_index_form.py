# Third-party imports
from django.core.files.uploadedfile import InMemoryUploadedFile
import pytest

# Local imports
from Blaster.forms.index_form import validate_index_form, IndexValidationEnum

valid_file = InMemoryUploadedFile(
    b"file_content", "field_name", "example.fasta",
    "text/plain", len(b"file_content"), "utf-8"
)


@pytest.mark.parametrize(
    "blast_mode, job_name, seq_text, seq_file, seq_file_text, "
    "expected_result",
    [
        # --- type protection ---
        (1, "", "atcg", None, "",
         IndexValidationEnum.INVALID_INPUT_TYPES),
        ("blastn", 1, "atcg", None, "",
         IndexValidationEnum.INVALID_INPUT_TYPES),
        ("blastn", "", 1, None, "",
         IndexValidationEnum.INVALID_INPUT_TYPES),
        ("blastn", "", "atcg", None, 1,
         IndexValidationEnum.INVALID_INPUT_TYPES),
        ("blastn", "", "atcg", 1, "",
         IndexValidationEnum.INVALID_FILE_OBJECT),

        # --- file processing ---
        ("blastn", "", "atcg", valid_file, "atcg",
         IndexValidationEnum.VALID),
        ("blastn", "", "atcg", None, "atcg",
         IndexValidationEnum.VALID),

        # --- blast options ---
        ("blastn", "", "atcg", None, "", IndexValidationEnum.VALID),
        ("blastp", "", "acac", None, "", IndexValidationEnum.VALID),
        ("blastrawr", "", "acac", None, "",
         IndexValidationEnum.INVALID_BLAST_MODE),

        # --- sequence absence ---
        ("blastn", "", "", None, "",
         IndexValidationEnum.MISSING_SEQUENCE_INPUT),
        ("blastn", "", "", valid_file, "",
         IndexValidationEnum.MISSING_SEQUENCE_INPUT),

        # --- sequence pattern blastn ---
        *[
            case
            for combo in ((
                ("blastn", "", sequence, None, "", expected_result),
                ("blastn", "", "", valid_file, sequence, expected_result),
            ) for sequence, expected_result in [
                ("atcg" * 100, IndexValidationEnum.VALID),
                ("atcg" * 100 + "b",
                 IndexValidationEnum.INVALID_SEQUENCE),
                ("bbb" * 100, IndexValidationEnum.INVALID_SEQUENCE),
                (">gene1\n" + "atcg" * 100, IndexValidationEnum.VALID),
                (">gene1\n" + "at\n\n\ncg" * 100,
                 IndexValidationEnum.VALID),
                (">gene1\n" + "at\r\n\r\n\r\ncg" * 100,
                 IndexValidationEnum.VALID),
                (">gene1\n" + "at\r\n\n\ncg" * 100,
                 IndexValidationEnum.VALID),
                (">gene1\nat\ncg", IndexValidationEnum.VALID),
                (
                ">gene1\n\n\n\n", IndexValidationEnum.INVALID_SEQUENCE),
                (" >gene1\natcg", IndexValidationEnum.INVALID_SEQUENCE),
                (
                " >gene1\natcg ", IndexValidationEnum.INVALID_SEQUENCE),
                (
                " >gene1\natcgb", IndexValidationEnum.INVALID_SEQUENCE),
                ])
            for case in combo
        ],

        # --- sequence pattern blastp ---
        *[
            case
            for combo in ((
                    ("blastp", "", sequence, None, "", expected_result),
                    ("blastp", "", "", valid_file, sequence, expected_result),
            ) for sequence, expected_result in [
                ("atcg", IndexValidationEnum.VALID),
                ("bbb", IndexValidationEnum.INVALID_SEQUENCE),
                (">gene1\natcg", IndexValidationEnum.VALID),
                (">gene1\nat\ncg", IndexValidationEnum.VALID),
                (" >gene1\natcg", IndexValidationEnum.INVALID_SEQUENCE),
            ])
            for case in combo
        ],

        # --- file sequence has priority ---
        ("blastn", "", "bbb", valid_file, "atcg",
         IndexValidationEnum.VALID),
    ]
)
def test_validate_index_form(
        blast_mode: str, job_name: str, seq_text: str,
        seq_file: InMemoryUploadedFile | None,
        seq_file_text: str, expected_result: IndexValidationEnum) -> None:
    """
    This unit test tests `validate_index_form`.
    It tests it by checking if the result of the validation
    is the expected result using the `IndexValidationEnum`.

    It has been paramatrized for this unittest to test all possible
    results.
    
    Tests:
        Invalid input type for every input.
        If it can process with a file, and with the absence of a file.
        Blast options are checked.
        That a sequence has to be present.
        The validation of the sequence itself:
            Allowed characters:
                dna/amino acids
                Enters
                Carriage returns
            Presence and absence of fasta format

            The sequence is validated for both sequences
            that could be used.

    Limitations:
        While it has been extensively parametrized, it
        only tests 1 or 2 variations of every "case" that 
        should individually affect the result.
        
        It doesn't test the length of inputs, nor does it 
        test the processing of longer sequences,
        as it's not possible for global strings to be too long.
        
            Notice:
            A seperate unittest should be created for validating
            with longer strings.

    :param blast_mode: The blast mode.
    :type blast_mode: str
    :param job_name: The job name.
    :type job_name: str
    :param seq_text: The sequence text.
    :type seq_text: str
    :param seq_file: The sequence file.
    :type seq_file: str
    :param seq_file_text: The sequence file text.
    :type seq_file_text: str
    :param expected_result: The expected result.
    :type expected_result: IndexValidationEnum
    :return: None.
    :rtype: None
    """
    result = validate_index_form(blast_mode, job_name, seq_text, seq_file,
                                 seq_file_text)

    assert result == expected_result
