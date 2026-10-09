import os
import subprocess
import re
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from src.agents.crew import (
    run_task_1_crew, 
    create_builder_agent, 
    get_project_building_task,
    create_resume_agent,
    create_ideation_agent,
    get_resume_task,
    get_email_rewrite_task
)
from crewai import Crew, Process

console = Console()

def clean_latex_output(raw_output: str) -> str:
    """Removes markdown code blocks from LLM output if present."""
    # Match ```latex ... ``` or ``` ... ``` and extract just the content
    match = re.search(r'```(?:latex)?(.*?)```', raw_output, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return raw_output.strip()

def compile_latex(company_name: str, tex_content: str):
    """Writes the tex content to a file and compiles it to PDF."""
    target_dir = f"resumes/{company_name.replace(' ', '_')}"
    os.makedirs(target_dir, exist_ok=True)
    
    tex_path = f"{target_dir}/resume.tex"
    with open(tex_path, "w") as f:
        f.write(tex_content)
        
    console.print(f"[cyan]Compiling LaTeX for {company_name}...[/cyan]")
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", target_dir, tex_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        console.print(f"[green]Resume PDF generated at: {target_dir}/resume.pdf[/green]")
        return True
    except FileNotFoundError:
        console.print("[red]Error: 'pdflatex' command not found. Please install BasicTeX/MacTeX.[/red]")
        return False
    except subprocess.CalledProcessError:
        console.print("[red]Error: LaTeX compilation failed. Check the syntax.[/red]")
        return False

def run_task_1(company: str, email: str, job_title: str):
    """
    Manual Interactive Orchestrator Flow.
    """
    console.print(f"\n[cyan]Step 1: Ideator Agent researching {company}...[/cyan]")
    
    try:
        ideation_result = run_task_1_crew(company, job_title)
        console.print(Markdown(str(ideation_result)))
    except Exception as e:
        console.print(f"[red]Error during ideation: {e}[/red]")
        return
    
    console.print("\n[bold yellow]Interactive Checkpoint: Project Selection[/bold yellow]")
    selected_project = console.input("Describe the chosen project to build (or type 'skip'): ")
    
    if selected_project.lower() != 'skip':
        console.print("\n[cyan]Step 2: Builder Agent generating code...[/cyan]")
        builder = create_builder_agent()
        build_task = get_project_building_task(builder, selected_project)
        
        build_crew = Crew(agents=[builder], tasks=[build_task], verbose=True)
        build_result = build_crew.kickoff()
        
        doc_path = f"projects/{company.replace(' ', '_')}_design.md"
        os.makedirs("projects", exist_ok=True)
        with open(doc_path, "w") as f:
            f.write(str(build_result))
        console.print(f"[green]Builder Agent completed! Design saved to {doc_path}[/green]")

    # Resume Feedback Loop
    console.print("\n[bold yellow]Interactive Checkpoint: Resume Approval[/bold yellow]")
    resume_approved = False
    
    # Dummy starting TeX template for the skeleton
    current_tex = "\\documentclass{article}\\begin{document}\\section{Experience}\\end{document}"
    
    # Initial generation of resume (with empty feedback to create the first draft)
    console.print("[cyan]Generating initial resume draft...[/cyan]")
    resume_agent = create_resume_agent()
    resume_task = get_resume_task(resume_agent, company, job_title, selected_project, current_tex, "Please write the initial draft based on the project.")
    resume_crew = Crew(agents=[resume_agent], tasks=[resume_task], verbose=True)
    raw_output = str(resume_crew.kickoff())
    current_tex = clean_latex_output(raw_output)

    while not resume_approved:
        compile_latex(company, current_tex)
        view_pdf = Confirm.ask("View the generated PDF?")
        if view_pdf:
            # On Mac, open the PDF
            pdf_path = f"resumes/{company.replace(' ', '_')}/resume.pdf"
            if os.path.exists(pdf_path):
                subprocess.run(["open", pdf_path])
        
        feedback = Prompt.ask("Provide feedback to change the resume (or type 'approve')")
        if feedback.lower() == 'approve':
            resume_approved = True
        else:
            console.print(f"[magenta]Sending feedback to Resume Agent: '{feedback}'...[/magenta]")
            resume_task = get_resume_task(resume_agent, company, job_title, selected_project, current_tex, feedback)
            resume_crew = Crew(agents=[resume_agent], tasks=[resume_task], verbose=True)
            console.print("[cyan]Regenerating resume...[/cyan]")
            raw_output = str(resume_crew.kickoff())
            current_tex = clean_latex_output(raw_output)

    # Email Feedback Loop
    console.print("\n[bold yellow]Interactive Checkpoint: Email Approval[/bold yellow]")
    email_approved = False
    
    # Extract email from the initial ideation result as a starting point if possible, otherwise start from scratch
    # In a fully robust system, you might extract the exact email, but we'll use a placeholder or ask the agent to write it.
    console.print("[cyan]Drafting initial outreach email...[/cyan]")
    ideator_agent = create_ideation_agent()
    email_task = get_email_rewrite_task(ideator_agent, company, email, job_title, "No current draft.", f"Write an initial cold email draft for the {job_title} role at {company}, mentioning the project: {selected_project}.")
    email_crew = Crew(agents=[ideator_agent], tasks=[email_task], verbose=True)
    current_email_body = str(email_crew.kickoff())
    
    while not email_approved:
        console.print(Panel(current_email_body, title=f"Draft for {email}"))
        feedback = Prompt.ask("Provide feedback to change the email (or type 'approve')")
        
        if feedback.lower() == 'approve':
            email_approved = True
        else:
            console.print(f"[magenta]Refining email based on: '{feedback}'...[/magenta]")
            email_task = get_email_rewrite_task(ideator_agent, company, email, job_title, current_email_body, feedback)
            email_crew = Crew(agents=[ideator_agent], tasks=[email_task], verbose=True)
            current_email_body = str(email_crew.kickoff())

    # Select Account and Send
    console.print("\n[bold yellow]Final Step: Sending Outreach[/bold yellow]")
    account = Prompt.ask("Select sending account", choices=["kushagraagarwal1612@gmail.com", "alt_account@gmail.com"], default="kushagraagarwal1612@gmail.com")
    
    console.print(f"[green]Sending email via {account} and logging to Google Sheets...[/green]")
    try:
        from src.tools.google_workspace import GoogleWorkspaceTool
        from dotenv import load_dotenv
        load_dotenv()
        
        gw = GoogleWorkspaceTool()
        gw.send_email(email, f"{job_title} - Kushagra Agarwal", current_email_body)
        
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        if sheet_id:
            gw.append_to_sheet(sheet_id, "Sheet1!A:E", [company, email, job_title, "Applied via Arachnid", selected_project])
            console.print(f"[bold green]Successfully logged application to {company} in tracker.[/bold green]")
    except Exception as e:
        console.print(f"[red]Google Workspace Error: {e}[/red]")

def run_task_2():
    """Automated Scraping Mode."""
    from src.tools.scraper import JobScraper
    from src.tools.google_workspace import GoogleWorkspaceTool
    from dotenv import load_dotenv
    import json

    load_dotenv()
    console.print("- Scraping Company Career Pages...")
    scraper = JobScraper()
    career_jobs = scraper.scrape_career_page("https://example-startup.com/careers")
    console.print("- Scraping YC Backed Startups...")
    yc_jobs = scraper.scrape_yc_jobs()
    
    new_jobs_count = len(career_jobs) + len(yc_jobs)
    console.print(f"[green]Found {new_jobs_count} new roles online. (Scraping simulation complete)[/green]")
    
    # 1. Intake: Read from Google Sheets
    console.print("\n[cyan]Checking Google Sheets for pending applications...[/cyan]")
    sheet_id = os.getenv("GOOGLE_SHEETS_ID")
    
    if not sheet_id:
        console.print("[red]GOOGLE_SHEETS_ID not set in .env. Skipping Google Sheets sync.[/red]")
        return
        
    try:
        gw = GoogleWorkspaceTool()
        # Assume columns: [Company, HR Email, Job Title, Status, Link]
        rows = gw.get_sheet_data(sheet_id, "Sheet1!A:E")
        
        if not rows:
            console.print("[yellow]No data found in the spreadsheet.[/yellow]")
            return
            
        header = rows[0]
        jobs_to_queue = []
        
        # 2. Filter: Select rows where Status == 'Not Applied'
        # Let's assume Status is the 4th column (index 3)
        for i, row in enumerate(rows[1:], start=2):
            if len(row) > 3 and row[3].strip().lower() == "not applied":
                company = row[0] if len(row) > 0 else "Unknown"
                hr_email = row[1] if len(row) > 1 else ""
                job_title = row[2] if len(row) > 2 else ""
                jobs_to_queue.append({
                    "row_index": i,
                    "company": company,
                    "email": hr_email,
                    "title": job_title
                })
                
        if not jobs_to_queue:
            console.print("[green]All caught up! No 'Not Applied' jobs found.[/green]")
            return
            
        console.print(f"[bold magenta]Found {len(jobs_to_queue)} jobs marked as 'Not Applied'.[/bold magenta]")
        
        # 3. Queue them for processing
        queue_file = "pending_jobs.json"
        
        # Load existing queue if any
        existing_queue = []
        if os.path.exists(queue_file):
            with open(queue_file, "r") as f:
                existing_queue = json.load(f)
                
        # Merge new jobs (avoiding exact duplicates)
        for job in jobs_to_queue:
            if not any(q["company"] == job["company"] and q["title"] == job["title"] for q in existing_queue):
                existing_queue.append(job)
                
        with open(queue_file, "w") as f:
            json.dump(existing_queue, f, indent=4)
            
        console.print(f"[green]Successfully queued {len(existing_queue)} jobs for processing![/green]")
        console.print("Run [bold cyan]emq review[/bold cyan] (or automated background worker) to process the queue.")
        
    except Exception as e:
        console.print(f"[red]Error syncing with Google Sheets: {e}[/red]")
