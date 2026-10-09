import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import time

app = typer.Typer(help="EMQ: Automated Job Application & Project Building System")
console = Console()

SPIDER_LOGO = """
[bold red]
           / _ \\
         \\_\\(_)/_/
          _//o\\\\_
           /   \\
[/bold red]
[bold white]        E M Q        [/bold white]
[dark_gray]Automated Career Agent[/dark_gray]
"""

def print_logo():
    console.clear()
    console.print(SPIDER_LOGO, justify="center")
    console.print("\n")

@app.command()
def apply():
    """
    Manual Mode: Interactive prompt to apply for a single job.
    """
    print_logo()
    
    console.print(Panel("[bold green]Welcome to EMQ Manual Mode.[/bold green]\nPlease provide the target details.", width=60))
    
    company = console.input("[bold cyan]Company Name:[/bold cyan] ")
    job_title = console.input("[bold cyan]Job Title:[/bold cyan] ")
    email = console.input("[bold cyan]HR/Recruiting Email:[/bold cyan] ")
    
    # Run the interactive orchestrator logic
    from src.orchestrator import run_task_1
    run_task_1(company, email, job_title)

@app.command()
def auto():
    """
    Automated Mode: Reads from Google Sheets and queues applications.
    """
    print_logo()
    console.print("[bold yellow]Initializing Automated Web Crawler & Sheet Sync...[/bold yellow]")
    
    from src.orchestrator import run_task_2
    run_task_2()
    
    console.print("[green]Scan complete. Check the Approval Dashboard for queued applications.[/green]")

@app.command()
def review():
    """
    Approval Dashboard: Review queued automated applications.
    """
    print_logo()
    console.print("[bold magenta]Fetching pending approvals from database...[/bold magenta]")
    
    queue_file = "pending_jobs.json"
    if os.path.exists(queue_file):
        import json
        with open(queue_file, "r") as f:
            queue = json.load(f)
        
        if queue:
            console.print(f"[green]Found {len(queue)} pending applications in the queue:[/green]")
            for item in queue:
                console.print(f"- [cyan]{item.get('title', 'Unknown')} at {item.get('company', 'Unknown')}[/cyan] (HR: {item.get('email', 'N/A')})")
            console.print("\n[yellow]To process these, run the orchestrator loop for each. (Future update will add full batch UI here)[/yellow]")
            return
            
    console.print("No pending applications to review right now.")

if __name__ == "__main__":
    app()
