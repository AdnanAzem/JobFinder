import click
from database.models import session, Resume
from api.job_fetcher import fetch_jobs
from nlp.job_matcher import rank_jobs

import click
from database.models import session, Resume
from api.job_fetcher import fetch_jobs
from nlp.job_matcher import rank_jobs

def search_jobs(resume_id, query, location):
    resume = session.query(Resume).filter_by(id=resume_id).first()
    if not resume:
        click.echo("Resume not found!")
        return

    jobs = fetch_jobs(query, location)
    ranked_jobs = rank_jobs(resume.skills, jobs)

    click.echo("\nTop Job Recommendations:")
    for job, score in ranked_jobs[:5]:
        click.echo(f"Title: {job['job_title']}, Company: {job['employer_name']}, Score: {score:.2f}")