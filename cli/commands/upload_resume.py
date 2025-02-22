import click
from database.models import session, Resume
from nlp.resume_parser import parse_resume

def upload_resume(file_path):
    try:
        # Parse the resume
        parsed_resume = parse_resume(file_path)
        
        # Save the resume to the database
        resume = Resume(file_path=file_path, content=parsed_resume["content"], skills=", ".join(parsed_resume["skills"]))
        session.add(resume)
        session.commit()
        
        click.echo(f"Resume uploaded successfully! ID: {resume.id}")
    except FileNotFoundError as e:
        click.echo(f"Error: {e}")
    except ValueError as e:
        click.echo(f"Error: {e}")
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")