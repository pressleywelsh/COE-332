import json
import logging
import os
import matplotlib.pyplot as plt
import numpy as np
from jobs import q, rd, rdb, results, get_job_by_id, start_job, update_job_status, save_result, JobStatus


logging.basicConfig(level=logging.DEBUG)

@q.worker
def do_work(jid: str) -> None:
    """
    Process a job ids and perform data analysis.

    This function:
    - Marks the job as started and updates its status to running
    - Retrieves data from Redis
    - Filters through data for ones  matching the country code and in the year range
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
        check = rd.get(key)
        if check is None:
            logging.warning(f"Skipping empty record for key {key}")
            continue

        try:
            record = json.loads(check)
        except json.JSONDecodeError:
            logging.warning(f"Skipping invalid JSON for key {key}")
            continue
        
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
    
    x_values = []
    y_values = []

    for record in matches:
        if record["health_exp"] is not None and record["life_expect"] is not None:
            x_values.append(record["health_exp"])
            y_values.append(record["life_expect"])

    if len(x_values) > 1:
        m, b = np.polyfit(x_values, y_values, 1)
        plt.plot(x_values, [m*x + b for x in x_values])

    plt.scatter(x_values, y_values)
    plt.xlabel('Health Expenditure')
    plt.ylabel('Life Expectancy')
    plt.title(f'Health Expenditure vs Life Expectancy ({country})')
    plt.savefig('/output_image.png')

    save_result(jid, result)

    with open('/output_image.png', 'rb') as f:
        img = f.read()

    rdb.hset(f"{jid}:image", "data", img)

    update_job_status(jid, JobStatus.SUCCESS)
    logging.info(f"Job {jid} completed successfully")



if __name__ == "__main__":
    do_work()
