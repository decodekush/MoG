import sys
import os
import json
import typer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ui import console, print_header, ask_select, ask_text, print_step, print_success
from rich.table import Table

app = typer.Typer(help="MOG: Automated Job Application & Project Building System", add_completion=False)

def apply():
    print_step("Entering Manual Application Mode\n")
    
    try:
        company = ask_text("Company Name:")
        job_title = ask_text("Job Title:")
        email = ask_text("HR/Recruiting Email:")
        
        # Run the interactive orchestrator logic
        from src.orchestrator import run_task_1
        run_task_1(company, email, job_title)
    except KeyboardInterrupt:
        console.print("\n[dim]Cancelled by user.[/dim]")
        sys.exit(0)

def auto():
    print_step("Entering Automated Scraping Mode\n")
    
    try:
        from src.orchestrator import run_task_2
        run_task_2()
    except KeyboardInterrupt:
        console.print("\n[dim]Cancelled by user.[/dim]")
        sys.exit(0)

def review():
    print_step("Entering Review Dashboard\n")
    
    queue_file = "pending_jobs.json"
    if os.path.exists(queue_file):
        with open(queue_file, "r") as f:
            queue = json.load(f)
        
        if queue:
            table = Table(show_header=True, header_style="bold green", border_style="dim", box=None)
            table.add_column("Job Title")
            table.add_column("Company")
            table.add_column("HR Email", style="dim")
            
            for item in queue:
                table.add_row(item.get('title', 'Unknown'), item.get('company', 'Unknown'), item.get('email', 'N/A'))
            
            console.print(table)
            console.print(f"\n[dim]Found {len(queue)} pending applications.[/dim]")
            console.print("[dim]To process these, run the manual flow for each.[/dim]")
            return
            
    print_success("[dim]No pending applications to review right now.[/dim]")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        print_header()
        
        try:
            console.print("[bold]What would you like to do?[/bold]\n")
            import questionary
            mode = ask_select(
                "", 
                choices=[
                    "Manual Apply (Interactive Flow)",
                    "Automated Scraping (Batch Sync)",
                    "Review Dashboard (Pending Apps)",
                    questionary.Separator(),
                    "Exit"
                ]
            )
            
            if mode == "Manual Apply (Interactive Flow)":
                apply()
            elif mode == "Automated Scraping (Batch Sync)":
                auto()
            elif mode == "Review Dashboard (Pending Apps)":
                review()
            else:
                sys.exit(0)
        except KeyboardInterrupt:
            console.print("\n[dim]Cancelled by user.[/dim]")
            sys.exit(0)

if __name__ == "__main__":
    app()
