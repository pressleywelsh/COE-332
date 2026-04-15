import jsonstart_job(jid)
import logging
import os
from jobs import q, rd, get_job_by_id, start_job, update_job_status, save_result, JobStatus


logging.basicConfig(level=logging.DEBUG)

@q.worker
def do_work(jid):
    """
    Process a job ids and perform data analysis.

    This function:
    - Marks the job as started and updates its status to running
    - Retrieves data from Redis
    - Filters through data for ones matching the country code and in the year range
    - Computes summary statistics: total number of matching records, average health expenditure, minimum and maximum life expectancy
    - Saves the result to the results database
    - Updates the job status to success

    Args:
    jid (str): The job id to process

    Returns:
    None
    """

    start_job(jid)
    logging.info(f"Worker started job {jid}")

    update_job_status(jid, JobStatus.RUNNING)

    keys = rd.keys()

    job = get_job_by_id(jid)
    country = job.country_code
    start = job.start_year
    end = job.end_year
    logging.debug(f"Job filters: country={country}, start={start}, end={end}")

    matches = []
    total = 0
    count=0
    life_vals = []
    for key in keys:
        record = json.loads(rd.get(key))
        if (record["country_code"] == country) and (record["year"] >= start) and (record["year"] <=end):
            matches.append(record)
            logging.debug(f"Match found for job {jid}: {record}")
            if record["health_exp"] is not None:
                total += record["health_exp"]
                count+=1
            if record["life_expect"] is not None:
                life_vals.append(record["life_expect"])
    logging.info(f"Found {len(matches)} matching records for job {jid}")
    if len(matches) == 0:
        logging.warning(f"No matching data found for job {jid}")

    avghealthexp = None
    if count > 0:
        avghealthexp = total / count
    
    min_life_expect = None
    max_life_expect = None
    if len(life_vals) > 0:
        min_life_expect = min(life_vals)
        max_life_expect = max(life_vals)
    logging.debug(f"Average health expenditure: {avghealthexp}")
    logging.debug(f"Min life expectancy: {min_life_expect}")
    logging.debug(f"Max life expectancy: {max_life_expect}")
        
    result = { "country_code": country, "start_year": start, "end_year": end, "count": len(matches), "min_life_expect": min_life_expect, "max_life_expect": max_life_expect, "avg_health_exp": avghealthexp}
    # compute averages or summary
    
    save_result(jid, result)
    logging.info(f"Saved result for job {jid}")

    update_job_status(jid, JobStatus.SUCCESS)
    logging.info(f"Job {jid} completed successfully")
