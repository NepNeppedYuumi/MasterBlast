# Standard library imports
from urllib.error import URLError

# Third-party imports
from Bio import Entrez
from Bio.Blast import NCBIWWW, NCBIXML
import Bio.Blast.Record

# Local imports
from Blaster.models import BlastJob, BlastHit, EntrezAccession, \
    EntrezAccessionCache, UnprocessedBlastJob
from Blaster.utils.queries import get_entrez_accession_from_code, \
    get_blast_job_from_id


def get_entrez_db_from_blast_program(program: str) -> str:
    """Converts a BLAST program to the corresponding Entrez database.

    Takes a BLAST program (blastn or blastp) and returns the Entrez
    database corresponding to possible hits from the BLAST job.

    :param program: BLAST program to convert.
    :type program: str.
    :raises ValueError: if the program is not blastn or blastp.
    :return: Entrez database corresponding to the BLAST program.
    :rtype: str
    """
    if program == 'blastn':
        return 'nucleotide'
    elif program == 'blastp':
        return 'protein'
    else:
        raise ValueError('Error: unsupported BLAST program')


def query_and_create_entrez_accession_cache(accession_code: str, db: str
                                            ) -> EntrezAccessionCache:
    """Performs Entrez queries for and stores GenBank & FASTA data.

    Takes an Entrez accession code and a database and performs two
    Entrez queries. The results of the queries, which may be GenBank or
    FASTA data, or error messages, will be stored in an 
    EntrezAccessionCache object and returned.

    :param accession_code: code to access an Entrez database entry.
    :type accession_code: str.
    :param db: Entrez database in which the entry is stored.
    :type db: str.
    :return: object containing GenBank and FASTA data.
    :rtype: EntrezAccessionCache.
    """
    genbank = perform_entrez_query(accession_code, db, 'gb', 'text')
    fasta = perform_entrez_query(accession_code, db, 'fasta', 'text')
    return EntrezAccessionCache.objects\
        .create_entrez_accession_cache(genbank, fasta)


def perform_entrez_query(accession: str, db: str, rettype: str, retmode: str) \
        -> str:
    """Performs an Entrez query using Bio.Entrez.efetch.

    Takes all the necessary arguments for Entrez.efetch (db, accession,
    rettype, retmode), performs the Entrez query and returns the result
    or an error message as a string.

    :param accession: the accession code for an entry in Entrez.
    :type accession: str.
    :param db: database to be queried.
    :type db: str.
    :param rettype: the type of content to be efetched.
    :type rettype: str.
    :param retmode: the format to return the content in.
    :return: query result or error message.
    :rtype: str.
    """
    Entrez.email = 'masterblast@bbc.com'
    try:
        with Entrez.efetch(
                db=db, id=accession, rettype=rettype,
                retmode=retmode) as handle:
            return handle.read()
    except URLError:
        return 'Error: a URLError occurred while executing Entrez query'
    except IOError:
        return 'Error: IOError occurred while executing Entrez query'
    except RuntimeError:
        return 'Error: a RuntimeError occurred while reading Entrez record'


def get_entrez_organism(accession: str, db: str) -> str:
    """Performs an Entrez query and gets the organism from the result.

    Takes an Entrez accession code and queries Entrez for an xml
    response of the entry. If there is an organism described in there,
    it is returned. Otherwise, the organism is deemed unknown.

    :param accession: code to access an Entrez database entry.
    :type accession: str.
    :param db: Entrez database in which the entry is stored.
    :type db: str.
    :return: organism if found, else unknown organism.
    :rtype: str.
    """
    xml = str(perform_entrez_query(accession, db, 'xml', 'xml'))

    if 'GBSeq_organism' in xml:
        return xml.split('<GBSeq_organism>')[1].split('</GBSeq_organism>')[0]
    else:
        return 'Unknown Organism'


def delete_unprocessed_blast_job(blast_job_id: int) -> None:
    """
    Removes an UnprocessedBlastJob from the database.

    Takes a BlastJob id and tries to retrieve and delete its 
    unprocessed counterpart from the database.

    :param blast_job_id: id of the UnprocessedBlastJob to delete.
    :type blast_job_id: int.
    """
    try:
        UnprocessedBlastJob.objects.get(job__pk=blast_job_id).delete()
    except UnprocessedBlastJob.DoesNotExist:
        pass
    except UnprocessedBlastJob.MultipleObjectsReturned:
        pass


def parse_blast_job_results(
        blast_job: BlastJob,
        record: Bio.Blast.Record,
        entrez_db: str
        ) -> None:
    """Creates BlastHit objects from a Bio.Blast.Record and BlastJob.

    Takes a BlastJob, a Bio.Blast.Record and Entrez database identifier
    and creates BlastHit objects from them. For each alignment in the
    record, the MasterBlast database is queried for an EntrezAccession.
    A new one is created if it doesn't exist yet. The alignment
    is skipped if no EntrezAccession can be retrieved or created.
    For each high-scoring segment pair in the alignment, a BlastHit is
    created.

    :param blast_job: BlastJob to parse the results of.
    :type blast_job: BlastJob.
    :param record: collection of alignments from BLAST.
    :type record: Bio.Blast.Record.
    :param entrez_db: Entrez database corresponding to the BlastJob.
    :type entrez_db: str.
    """
    for alignment in record.alignments:
        organism = get_entrez_organism(alignment.accession, entrez_db)
        description = ' '.join(alignment.title.split(' ')[1::])

        # Try to get EntrezAccession from Django db.
        try:
            accession = get_entrez_accession_from_code(alignment.accession)
        
        # Create a new one if it doesn't exist.
        except EntrezAccession.DoesNotExist:
            accession = EntrezAccession.objects\
                .create_entrez_accession(alignment.accession, organism)
        
        # Skip the alignment if an EntrezAccession cannot be created.
        except ValueError:
            continue

        for hsp in alignment.hsps:
            BlastHit.objects.create_hit(
                blast_job_id=blast_job.id,
                accession_id=accession.id,
                description=description,
                blast_score=hsp.score,
                bit_score=hsp.bits,
                e_value=hsp.expect,
                identities=hsp.identities,
                align_length=hsp.align_length,
                query_start=hsp.query_start,
                query_end=hsp.query_end,
                query_length=len(blast_job.sequence),
                subject_seq=hsp.sbjct,
                subject_start=hsp.sbjct_start,
                subject_end=hsp.sbjct_end
            )


def perform_blast_job(blast_job_id: int) -> None:
    """Queries NCBI BLAST using NCBIWWW.qblast and stores the result.

    Takes a BlastJob id and performs the BLAST job using NCBIWWW,
    NCBIXML and get_entrez_db_from_blast_program. If an error occurs, 
    the BLAST job will be given an informative message as their
    error_msg attribute. The resulting records are parsed if no errors
    occurred.

    :param blast_job_id: identifier for the BlastJob.
    :type blast_job_id: int.
    """
    blast_job = get_blast_job_from_id(blast_job_id)

    try:
        # Depending on where the BLAST job fails, the error_msg is set
        error_msg = 'Failed: the BLAST job could not be executed.'
        handle = NCBIWWW.qblast(blast_job.program, "nr", blast_job.sequence)

        error_msg = 'Failed: the BLAST job result could not be read.'
        record = NCBIXML.read(handle)

        error_msg = 'Failed: the Entrez database could not be found.'
        entrez_db = get_entrez_db_from_blast_program(blast_job.program)
    except ValueError:
        # Only when something goes wrong, the error_msg is stored in
        # the BlastJob
        delete_unprocessed_blast_job(blast_job_id)
        blast_job.error_msg = error_msg
        blast_job.save()
        return
    except:
        delete_unprocessed_blast_job(blast_job_id)

    try:
        parse_blast_job_results(blast_job, record, entrez_db)
    except:
        pass
    finally:
        delete_unprocessed_blast_job(blast_job_id)
