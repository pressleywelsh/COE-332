import time
from jobs import q, start_job, update_job_status, JobStatus


@q.worker
def do_work(jid):
    """
    Processes job IDs
    """
    update_job_status(jid, JobStatus.RUNNING)

    keys = rd.keys()

    job = get_job_by_id(jid)
    
    country = job.country_code
    start = job.start_year
    end = job.end_year
    
    matches = []
    total = 0
    count=0
    life_vals = []
    for key in keys:
        record = json.loads(rd.get(key))
        if (record["country_code"] == country) and (record["year"] >= start) and (record["year"] <=end):
            matches.append(record)
            if record["health_exp"] is not None:
                total += record["health_exp"]
                count+=1
            if record["life_expect"] is not None:
                life_vals.append(record["life_expect"])

    avghealthexp = None
    if count > 0:
        avghealthexp = total / count
    
    min_life_expect = None
    max_life_expect = None
    if len(life_vals) > 0:
        min_life_expect = min(life_vals)
        max_life_expect = max(life_vals)
    
    result = { "country_code": country, "start_year": start, "end_year": end, "count": len(matches), "min_life_expect": min_life_expect, "max_life_expect": max_life_expect, "avg_health_exp": avghealthexp}
    # compute averages or summary
    
    save_result(jid, result)


    update_job_status(jid, JobStatus.SUCCESS)

do_work()
