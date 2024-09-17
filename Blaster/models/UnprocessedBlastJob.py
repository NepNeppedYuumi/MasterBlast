# Third-party imports
from django.db import models


class UnprocessedBlastJob(models.Model):
    """A BLAST query that is still running

    When a BlastJob object is created, an UnprocessedBlastJob
    counterpart is also created. When the results of the query are
    received, the UnprocessedBladJob is removed.

    :param models: _description_
    :type models: _type_
    :return: _description_
    :rtype: _type_
    """
    job = models.ForeignKey(
        "BlastJob",
        on_delete=models.CASCADE
    )

    @classmethod
    def check_blast_job_is_processed(cls, job_id: int) -> bool:
        """
        Checks if a blast job has been processed. If a job has not
        been processed yet, it will return False. If a job has been
        processed, it will return True. Searching will be done using a
        BlastJob id.

        :param job_id: identifier for the UnprocessedBlastJob
        :return: True when the UnprocessedBlastJob has been processed
        :rtype: bool
        """
        return not UnprocessedBlastJob.objects.filter(job__pk=job_id).exists()

    @classmethod
    def remove_by_blast_job(cls, blast_job_id: int) -> None:
        """Removes an UnprocessedBlastJob with from the database by id

        :param blast_job_id: identifier for the UnprocessedBlastJob
        :type blast_job_id: int
        """
        UnprocessedBlastJob.objects.get(job__pk=blast_job_id).delete()
