from src import jobs
from jobs import JobStatus


def test_add_job():
    job = jobs.add_job("USA", 2000, 2005)

    assert job.country_code == "USA"
    assert job.status == JobStatus.QUEUED


def test_get_job_by_id():
    job = jobs.add_job("USA", 2000, 2005)
    result = jobs.get_job_by_id(job.jid)

    assert result.jid == job.jid


def test_update_job_status():
    job = jobs.add_job("USA", 2000, 2005)

    jobs.update_job_status(job.jid, JobStatus.RUNNING)
    updated = jobs.get_job_by_id(job.jid)

    assert updated.status == JobStatus.RUNNING


def test_results():
    jobs.save_result("abc123", {"count": 3})
    result = jobs.get_result("abc123")

    assert result["count"] == 3
