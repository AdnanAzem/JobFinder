import click
from database.models import session, Resume
from nlp.resume_parser import parse_resume
from sqlalchemy import text

def check_and_truncate_resumes():
    # Check the number of rows in the resumes table
    row_count = session.query(Resume).count()
    
    # If there are 25 or more rows, truncate the table
    if row_count >= 25:
        session.execute(text("TRUNCATE TABLE resumes RESTART IDENTITY"))
        session.commit()
        print("Resumes table truncated.")

def upload_resume(file_path):
    try:
        # Check and truncate the resumes table if necessary
        check_and_truncate_resumes()

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