import time
from jobs import q, start_job, update_job_status, JobStatus


@q.worker
def do_work(jid):
    """
    Processes job IDs
    """
    start_job(jid)
    update_job_status(jid, JobStatus.RUNNING)
    time.sleep(5)
    update_job_status(jid, JobStatus.SUCCESS)


do_work()
