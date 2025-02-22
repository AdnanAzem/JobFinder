import click
from cli.commands.upload_resume import upload_resume
from cli.commands.search_jobs import search_jobs

@click.group()
def cli():
    pass

@cli.command()
def start():
    """Start the interactive job finder."""
    while True:
        click.echo("\n--- AI-Powered Job Finder ---")
        click.echo("1. Upload Resume")
        click.echo("2. Search Jobs")
        click.echo("3. Exit")
        choice = click.prompt("Choose an option", type=int)

        if choice == 1:
            while True:
                file_path = click.prompt("Enter the path to your resume (PDF)")
                try:
                    upload_resume(file_path)
                    break  # Exit the loop if the upload is successful
                except Exception as e:
                    click.echo(f"Error: {e}")
                    retry = click.prompt("Would you like to try again? (yes/no)", default="yes")
                    if retry.lower() != "yes":
                        break
        elif choice == 2:
            resume_id = click.prompt("Enter your resume ID", type=int)
            query = click.prompt("Enter job title (e.g., Software Engineer)")
            location = click.prompt("Enter location (e.g., Israel)")
            search_jobs(resume_id, query, location)
        elif choice == 3:
            click.echo("Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please try again.")