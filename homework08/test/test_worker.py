from src import jobs
from src import worker


def test_do_work():
    job = jobs.add_job("USA", 2000, 2005)

    worker.do_work(job.jid)
    result = jobs.get_result(job.jid)

    assert isinstance(result, dict)
    assert result["country_code"] == "USA"
    assert "count" in result
