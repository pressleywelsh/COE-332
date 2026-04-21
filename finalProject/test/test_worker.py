from src import jobs
from src import worker


def test_do_work():
    job = jobs.add_job("USA", 2000, 2005)

    worker.do_work.__wrapped__(job.jid) #used ai here to fix error i couldnt solve

    updated_job = jobs.get_job_by_id(job.jid)
    assert updated_job.status == jobs.JobStatus.SUCCESS
