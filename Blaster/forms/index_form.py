# Standard library imports
from enum import Enum, auto
import re

# Third-party imports
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError


class IndexValidationEnum(Enum):
    """
    This enum serves as the validation status of the index form.
    All possible evaluations for inputs of the index form
    are categorized in this enum.
    If the inputs are not considered valid, the enum name
    can be used to describe why the inputs are not valid.
    """
    VALID = auto()
    INVALID_INPUT_TYPES = auto()
    INVALID_FILE_OBJECT = auto()
    # INVALID_FILE_EXTENSION = auto()
    INVALID_BLAST_MODE = auto()
    MISSING_SEQUENCE_INPUT = auto()
    INVALID_SEQUENCE = auto()


def read_index_file(seq_file: InMemoryUploadedFile | None) -> str:
    """
    It will attempt to read and parse the contents of the file 
    provided to the index form as a string.
    If no file is provided, it will simply return an empty string.

    The file type provided is irrelevant, the file will simply
    be read and an attempt to decode the content will be done
    using django's `smart_str`.
    In case the file cannot be decoded to a str by the method,
    it will return an empty string instead.

    As a result of `InMemoryUploadedFile` function as a generator,
    it is impossible with the current implementation to identify
    if the file content was empty, or could not be decoded to a string.

    As a result of not checking the file extension, and using smart_str
    it is could be possible that the content of a file 
    could be altered, or misread. 
    Testing is required to identify when this would happen.

    :param seq_file: The file provided to the index form.
    :type seq_file: InMemoryUploadedFile or None
    :return: The contents of the file, or an empty string.
    :rtype: str
    """
    try:
        if type(seq_file) is InMemoryUploadedFile:
            return smart_str(seq_file.read())
    except DjangoUnicodeDecodeError:
        pass
    return ""


def validate_index_form(
        blast_mode: str, job_name: str, seq_text: str,
        seq_file: InMemoryUploadedFile | None,
        seq_file_text: str) -> IndexValidationEnum:
    """
    Validates all the possible inputs to the form that are known
    to be accepted. Any inputs that do not match, will return
    an Enum value other than 1
    An Enum value of 1 means the form was successfully filled.

    The validator expects for the content of the seq_file to have been
    read beforehand and passed on as a string separately.

    A sequence is considered a valid sequence if it
    has a sequence with only valid characters,
    defined by the blast type.
    Currently ambiguous characters are not included
    A sequence can be split over multiple lines through \n or \r\n
    A sequence can be preceded with a header but does not need one,
    defined under the fasta standards as >....\n

    A sequence input can only consist of a singular input with the
    entire content of the input following the allowed standard.

    Any file extension can be considered a valid file, as long
    as the data in the file can be encoded to strings.

    If a file with content is submitted, and a seq_text only the
    file is checked and processed.

    :param blast_mode: The blast mode selected
    :type blast_mode str
    :param job_name: The name of the job
    :type job_name str
    :param seq_text: The sequence as string
    :type seq_text str
    :param seq_file: The file that has been provided
    :type seq_file InMemoryUploadedFile | None
    :param seq_file_text: The sequence from the file
    :return:
    :rtype: IndexValidationEnum
    """
    if any(type(i) is not str for i in
           (blast_mode, job_name, seq_text, seq_file_text)):
        return IndexValidationEnum.INVALID_INPUT_TYPES

    if (seq_file is not None and
            type(seq_file) is not InMemoryUploadedFile):
        return IndexValidationEnum.INVALID_FILE_OBJECT

    # # commented out as it's not behaviour the client has requested
    # if type(seq_file) is InMemoryUploadedFile:
    #     if any(not seq_file.name.endswith(i) for i in (".fasta",)):
    #         return IndexValidationEnum.INVALID_FILE_EXTENSION

    if blast_mode not in ("blastn", "blastp"):
        return IndexValidationEnum.INVALID_BLAST_MODE

    if seq_text == "" and seq_file_text == "":
        return IndexValidationEnum.MISSING_SEQUENCE_INPUT

    sequence = ""
    if type(seq_file) is InMemoryUploadedFile and seq_file_text != "":
        sequence = seq_file_text
    elif seq_text != "":
        sequence = seq_text

    characters = ""
    if blast_mode == "blastn":
        characters = "atcg"
    elif blast_mode == "blastp":
        characters = "acdefghiklmnpqrstvwy"
    pattern = rf"(?i)" \
              rf"^(>.+(\n|\r\n))?" \
              rf"(?>[{characters}]+(\n|\r\n)*)+$"

    if not re.match(pattern, sequence):
        return IndexValidationEnum.INVALID_SEQUENCE

    return IndexValidationEnum.VALID


def process_index_form(
        seq_text: str, seq_file: InMemoryUploadedFile | None,
        seq_file_text: str) -> tuple[str, str]:
    """
    Processes the contents of the index form
    to allow for uniform usage by different parts of the application.
    Usage of this function is required when dealing with user input
    data from the form.

    It selects which sequence to keep.

    It replaces all carriage returns for escape characters.
    This is to support different file formats, and text input
    on the form produces carriage returns.

    In case a fasta header is present, the header and
    sequence are split from each other.
    In case no fasta header is present the header is an empty string.

    All enters from the sequence are removed.

    :param seq_text: The sequence text.
    :type seq_text str
    :param seq_file: The sequence file.
    :type seq_file InMemoryUploadedFile or None
    :param seq_file_text: The sequence text from the file.
    :type seq_file_text str
    :return: A tuple containing the header and the cleaned up sequence.
    :rtype: tuple[str, str]
    """
    if type(seq_file) is InMemoryUploadedFile:
        sequence = seq_file_text
    else:
        sequence = seq_text
    sequence = sequence.replace("\r\n", "\n")

    if sequence.startswith(">"):
        header, *sequence = sequence[1:].rstrip("\n").split("\n")
        return header, "".join(sequence)
    return "", sequence.replace("\n", "")
