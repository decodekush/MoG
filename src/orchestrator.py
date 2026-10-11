import os
import time
import subprocess
import re
from src.ui import console, ask_text, ask_select, print_step, print_success, print_error, status
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

# Set to True to bypass API calls for testing the UI flow
MOCK_MODE = True



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
        
    console.print(f"[dim white]Compiling LaTeX for {company_name}...[/dim white]")
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", target_dir, tex_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        console.print(f"[dim white]Resume PDF generated at: {target_dir}/resume.pdf[/dim white]")
        return True
    except FileNotFoundError:
        print_error("Error: 'pdflatex' command not found. Please install BasicTeX/MacTeX.")
        return False
    except subprocess.CalledProcessError:
        print_error("Error: LaTeX compilation failed. Check the syntax.")
        return False

def get_claude_style():
    from questionary import Style
    return Style([
        ('qmark', 'fg:#888888'),
        ('question', 'bold'),
        ('answer', 'fg:#cccccc'),
        ('pointer', 'fg:#ffffff bold'),
        ('highlighted', 'fg:#ffffff bold'),
        ('selected', 'fg:#ffffff'),
        ('separator', 'fg:#555555'),
        ('instruction', 'fg:#666666'),
        ('text', ''),
    ])

def run_task_1(company: str, email: str, job_title: str):
    """
    Manual Interactive Orchestrator Flow.
    """
    import questionary
    style = get_claude_style()
    
    console.print(f"\n[dim]❯ Ideator Agent researching {company}...[/dim]")
    
    try:
        if MOCK_MODE:
            time.sleep(2)
            ideation_result = f"**[MOCK]** Company Research for {company}:\n- Great culture\n- Needs Python devs\n\n**Proposed Projects:**\n1. Payment Gateway Integration\n2. Real-time Dashboard"
        else:
            ideation_result = run_task_1_crew(company, job_title)
        console.print("")
        console.print(Markdown(str(ideation_result)))
        console.print("")
    except Exception as e:
        print_error(f"Error during ideation: {e}")
        return
    
    project_action = ask_select("❯ Email drafted. What would you like to do?", choices=[
            "Provide my own project idea",
            "Use Option 1 from above",
            "Use Option 2 from above",
            "Skip project building"
        ])
    
    if not project_action:
        return
        
    selected_project = "skip"
    if project_action == "Provide my own project idea":
        selected_project = ask_text("❯ Describe the project to build:")
    elif project_action == "Use Option 1 from above":
        selected_project = "Option 1 from the ideation result"
    elif project_action == "Use Option 2 from above":
        selected_project = "Option 2 from the ideation result"
        
    if selected_project and selected_project.lower() != 'skip':
        console.print(f"\n[dim]❯ Builder Agent generating code for '{selected_project}'...[/dim]")
        if MOCK_MODE:
            time.sleep(2)
            build_result = f"**[MOCK]** Project Design for {selected_project}:\n- Architecture: Microservices\n- Tools: Python, FastAPI"
        else:
            builder = create_builder_agent()
            build_task = get_project_building_task(builder, selected_project)
            build_crew = Crew(agents=[builder], tasks=[build_task], verbose=True)
            build_result = build_crew.kickoff()
        
        doc_path = f"projects/{company.replace(' ', '_')}_design.md"
        os.makedirs("projects", exist_ok=True)
        with open(doc_path, "w") as f:
            f.write(str(build_result))
        print_success(f"Builder Agent completed! Design saved to {doc_path}")

    # Resume Feedback Loop
    console.print("\n[bold]Resume Approval[/bold]")
    resume_approved = False
    
    # Dummy starting TeX template for the skeleton
    current_tex = "\\documentclass{article}\\begin{document}\\section{Experience}\\end{document}"
    
    print_step("Generating initial resume draft...")
    if MOCK_MODE:
        time.sleep(2)
        raw_output = "\\documentclass{article}\\begin{document}\\section{Experience}\\item Built a cool project.\\end{document}"
    else:
        resume_agent = create_resume_agent()
        resume_task = get_resume_task(resume_agent, company, job_title, selected_project, current_tex, "Please write the initial draft based on the project.")
        resume_crew = Crew(agents=[resume_agent], tasks=[resume_task], verbose=True)
        raw_output = str(resume_crew.kickoff())
    current_tex = clean_latex_output(raw_output)

    while not resume_approved:
        compile_latex(company, current_tex)
        
        action = ask_select("❯ Email drafted. What would you like to do?", choices=[
                "View PDF",
                "Provide Feedback to Agent",
                "Approve and Continue"
            ])
        
        if not action:
            return
            
        if action == "View PDF":
            pdf_path = f"resumes/{company.replace(' ', '_')}/resume.pdf"
            if os.path.exists(pdf_path):
                subprocess.run(["open", pdf_path])
        elif action == "Approve and Continue":
            resume_approved = True
            print_success("Resume approved.")
        elif action == "Provide Feedback to Agent":
            feedback = ask_text("❯ Enter feedback for the Resume Agent:")
            if feedback:
                print_step(f"Sending feedback to Resume Agent: '{feedback}'...")
                if MOCK_MODE:
                    time.sleep(2)
                    raw_output = f"\\documentclass{{article}}\\begin{{document}}\\section{{Experience}}\\item Built a cool project.\\item Feedback applied: {feedback}\\end{{document}}"
                else:
                    resume_task = get_resume_task(resume_agent, company, job_title, selected_project, current_tex, feedback)
                    resume_crew = Crew(agents=[resume_agent], tasks=[resume_task], verbose=True)
                    print_step("Regenerating resume...")
                    raw_output = str(resume_crew.kickoff())
                current_tex = clean_latex_output(raw_output)

    # Email Feedback Loop
    console.print("\n[bold]Email Approval[/bold]")
    email_approved = False
    
    print_step("Drafting initial outreach email...")
    if MOCK_MODE:
        time.sleep(1)
        current_email_body = f"Hi {company} team,\n\nI am applying for {job_title}. I recently built {selected_project}.\n\nBest,\nKushagra"
    else:
        ideator_agent = create_ideation_agent()
        email_task = get_email_rewrite_task(ideator_agent, company, email, job_title, "No current draft.", f"Write an initial cold email draft for the {job_title} role at {company}, mentioning the project: {selected_project}.")
        email_crew = Crew(agents=[ideator_agent], tasks=[email_task], verbose=True)
        current_email_body = str(email_crew.kickoff())
    
    while not email_approved:
        console.print("")
        console.print(Markdown(current_email_body))
        console.print("")
        
        action = ask_select("❯ Email drafted. What would you like to do?", choices=[
                "Provide Feedback to Agent",
                "Approve and Continue"
            ])
        
        if not action:
            return
            
        if action == "Approve and Continue":
            email_approved = True
            print_success("Email approved.")
        elif action == "Provide Feedback to Agent":
            feedback = ask_text("❯ Enter feedback for the Ideator Agent:")
            if feedback:
                print_step(f"Refining email based on: '{feedback}'...")
                if MOCK_MODE:
                    time.sleep(1)
                    current_email_body += f"\n\n(Updated based on feedback: {feedback})"
                else:
                    email_task = get_email_rewrite_task(ideator_agent, company, email, job_title, current_email_body, feedback)
                    email_crew = Crew(agents=[ideator_agent], tasks=[email_task], verbose=True)
                    current_email_body = str(email_crew.kickoff())

    # Select Account and Send
    console.print("\n[bold]Final Step: Sending Outreach[/bold]")
    
    account = ask_select("❯ Select sending account:", choices=["kushagraagarwal1612@gmail.com", "alt_account@gmail.com"])
    
    if not account:
        print_error("No account selected. Aborting.")
        return

    print_step(f"Sending email via {account} and logging to Google Sheets...")
    try:
        if MOCK_MODE:
            time.sleep(2)
            print_success(f"[MOCK] Successfully logged application to {company} in tracker.")
        else:
            from src.tools.google_workspace import GoogleWorkspaceTool
            from dotenv import load_dotenv
            load_dotenv()
            
            gw = GoogleWorkspaceTool()
            gw.send_email(email, f"{job_title} - Kushagra Agarwal", current_email_body)
            
            sheet_id = os.getenv("GOOGLE_SHEETS_ID")
            if sheet_id:
                gw.append_to_sheet(sheet_id, "Sheet1!A:E", [company, email, job_title, "Applied via MOG", selected_project])
                print_success(f"Successfully logged application to {company} in tracker.")
    except Exception as e:
        print_error(f"Google Workspace Error: {e}")

def run_task_2():
    """Automated Scraping Mode."""
    from src.tools.scraper import JobScraper
    from src.tools.google_workspace import GoogleWorkspaceTool
    from dotenv import load_dotenv
    import json

    load_dotenv()
    print_step("Scraping Company Career Pages...")
    if MOCK_MODE:
        time.sleep(1)
        career_jobs = ["Job 1", "Job 2"]
        print_step("Scraping YC Backed Startups...")
        time.sleep(1)
        yc_jobs = ["Job 3"]
    else:
        scraper = JobScraper()
        career_jobs = scraper.scrape_career_page("https://example-startup.com/careers")
        print_step("Scraping YC Backed Startups...")
        yc_jobs = scraper.scrape_yc_jobs()
    
    new_jobs_count = len(career_jobs) + len(yc_jobs)
    print_success(f"Found {new_jobs_count} new roles online. (Scraping simulation complete)")
    
    # 1. Intake: Read from Google Sheets
    print_step("Checking Google Sheets for pending applications...")
    sheet_id = os.getenv("GOOGLE_SHEETS_ID")
    
    if not sheet_id and not MOCK_MODE:
        print_error("GOOGLE_SHEETS_ID not set in .env. Skipping Google Sheets sync.")
        return
        
    try:
        if MOCK_MODE:
            time.sleep(1)
            rows = [
                ["Company", "HR Email", "Job Title", "Status"],
                ["Mock Startup Inc.", "hr@mockstartup.com", "Software Engineer", "Not Applied"],
                ["Big Tech Corp", "recruiter@bigtech.com", "Backend Dev", "Applied"]
            ]
        else:
            gw = GoogleWorkspaceTool()
            # Assume columns: [Company, HR Email, Job Title, Status, Link]
            rows = gw.get_sheet_data(sheet_id, "Sheet1!A:E")
        
        if not rows:
            print_error("No data found in the spreadsheet.")
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
            print_success("All caught up! No 'Not Applied' jobs found.")
            return
            
        print_step(f"Found {len(jobs_to_queue)} jobs marked as 'Not Applied'.")
        
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
            
        print_success(f"Successfully queued {len(existing_queue)} jobs for processing!")
        print_step("Run mog and select 'Review Dashboard' to process the queue.")
        
    except Exception as e:
        print_error(f"Error syncing with Google Sheets: {e}")
