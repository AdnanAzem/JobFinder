import requests
from dotenv import load_dotenv
import os
from database.models import session, JobListing

load_dotenv()

def fetch_jobs(query, location):
    api_key = os.getenv("JSEARCH_API_KEY")
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {"query": f"{query} in {location}", "page": "1", "num_pages": "1"}
    response = requests.get(url, headers=headers, params=params)
    jobs = response.json().get("data", [])
    
    # Save jobs to the database
    save_jobs_to_db(jobs)
    
    return jobs

def save_jobs_to_db(jobs):
    for job in jobs:
        job_listing = JobListing(
            title=job.get("job_title"),
            description=job.get("job_description"),
            company=job.get("employer_name"),
            location=job.get("job_country")
        )
        session.add(job_listing)
    session.commit()