from datetime import datetime
import json
import uuid
import redis
from hotqueue import HotQueue
from enum import Enum
from pydantic import BaseModel
import typing
import os
import logging


logging.basicConfig(level=logging.DEBUG)
_redis_ip = os.environ.get("REDIS_IP", "redis-db")
_redis_port = 6379

rd = redis.Redis(host=_redis_ip, port=_redis_port, db=0, decode_responses=True)
q = HotQueue("queue", host=_redis_ip, port=_redis_port, db=1)
jdb = redis.Redis(host=_redis_ip, port=_redis_port, db=2, decode_responses=True)
rdb = redis.Redis(host=_redis_ip, port=_redis_port, db=3, decode_responses=True)


class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    ERROR = "FINISHED -- ERROR"
    SUCCESS = "FINISHED -- SUCCESS"

class Job(BaseModel):
    jid: str
    status: JobStatus
    country_code: str
    start_year: int
    end_year: int
    start_time: typing.Optional[datetime] = None
    end_time: typing.Optional[datetime] = None
    model_config = {"use_enum_values": True} #used ai here to fix warning from pytest


def _generate_jid() -> str:
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())

def _instantiate_job(jid: str, status: JobStatus, country_code: str, start_year: int, end_year: int) -> Job:
    """
    Create the job object description.
    """
    return Job(
            jid=jid,
            status=status,
            country_code=country_code,
            start_year=start_year,
            end_year=end_year,
            start_time=None,
            end_time=None
            )

def _save_job(jid: str, job: Job) -> bool:
    """
    Save a job object in the Redis database.
    """
    jdb.set(jid, json.dumps(job.model_dump(mode="json")))
    logging.debug(f"Saved job {jid} to jobs database")
    return True

def _queue_job(jid: str) -> bool:
    """
    Add a job to the Redis queue.
    """
    q.put(jid)
    logging.info(f"Queued job {jid}")
    return True

def get_job_by_id(jid: str) -> Job | None:
    """Return job object given jid."""
    raw_data = jdb.get(jid)
    if raw_data is None:
        logging.warning(f"Job {jid} not found")
        return None

    logging.debug(f"Retrieved job {jid}")
    return Job(**json.loads(raw_data))

def get_job_ids() -> list[str]:
    """Return all job IDs"""
    logging.debug(f"Retrieving all job ids")
    return jdb.keys()

def add_job(country_code: str, start_year: int, end_year: int) -> Job:
    """Add a job to the redis database and queue."""
    jid = _generate_jid()
    job = _instantiate_job(jid, JobStatus.QUEUED, country_code, start_year, end_year)
    _save_job(jid, job)
    _queue_job(jid)
    logging.info(f"Creating job for {country_code} from {start_year} to {end_year}")
    return job

def start_job(jid: str) -> bool:
    """Called by worker when starting a new job. Updates start time."""
    start_time = datetime.now()
    job = get_job_by_id(jid)
    if job is None:
        logging.warning(f"Job {jid} not found")
        return False
    job.start_time = start_time
    logging.info(f"Starting job {jid}")
    return _save_job(jid=jid, job=job)

def update_job_status(jid: str, status: JobStatus) -> bool | None:
    """Update job status."""
    job = get_job_by_id(jid)
    logging.info(f"Updating job {jid} to status {status}")
    if job is None:
        logging.warning(f"Job {jid} not found")
        return None
    job.status = status
    if job.status == JobStatus.ERROR or job.status == JobStatus.SUCCESS:
        job.end_time = datetime.now()

    return _save_job(jid, job)

def save_result(jid: str, result: dict) -> bool:
    """
    Save a completed job result in the results Redis database.
    """
    rdb.set(jid, json.dumps(result))
    logging.info(f"Saved result for job {jid}")
    return True

def get_result(jid: str) -> typing.Optional[dict]:
    """
    Return saved result for a given job id.
    """
    raw_data = rdb.get(jid)
    if raw_data is None:
        logging.warning(f"No result found for job {jid}")
        return None

    logging.debug(f"Retrieved result for job {jid}")
    return json.loads(raw_data)
