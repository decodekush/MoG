import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

# We can pass the litellm model string directly to CrewAI
# It automatically picks up GEMINI_API_KEY from .env
llm_model = "gemini/gemini-3.1-pro-preview"

def load_skill(filename: str) -> str:
    """Helper to load instructions from the SKILL.md files"""
    skill_path = os.path.join(os.path.dirname(__file__), '..', 'skills', filename)
    try:
        with open(skill_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Skill file not found. Please ensure it exists."

# ---------------------------------------------------------
# AGENT DEFINITIONS
# ---------------------------------------------------------

def create_ideation_agent():
    return Agent(
        role="Principal Career Strategist & Tech Outreach Specialist",
        goal="Research companies, identify technical gaps in the candidate's profile, propose highly-targeted projects, and draft cold outreach emails.",
        backstory=f"You are following these strict guidelines for Kushagra's outreach:\n\n{load_skill('project_ideation_and_email.md')}",
        verbose=True,
        allow_delegation=False,
        llm=llm_model
    )

def create_builder_agent():
    return Agent(
        role="Senior Staff Software Engineer & Architect",
        goal="Design and scaffold a high-quality, portfolio-grade software project from an idea to a shipped repo with proper LLD, HLD, and tests.",
        backstory=f"You are following these strict engineering guidelines:\n\n{load_skill('project_building.md')}",
        verbose=True,
        allow_delegation=False,
        llm=llm_model
    )

def create_resume_agent():
    return Agent(
        role="Expert Technical Recruiter & ATS Optimizer",
        goal="Format and optimize the candidate's technical resume, writing bullet points using the XYZ formula.",
        backstory=f"You are following these ATS optimization guidelines:\n\n{load_skill('ats_optimizer.md')}",
        verbose=True,
        allow_delegation=False,
        llm=llm_model
    )

# ---------------------------------------------------------
# TASK CREATORS FOR WORKFLOW 1
# ---------------------------------------------------------

def get_ideation_task(agent, company: str, job_title: str):
    return Task(
        description=f"Research {company} for the {job_title} role. Perform a fit and gap analysis for Kushagra. Propose 2 new projects and draft 2 versions of the cold email according to your instructions.",
        expected_output="A Markdown document containing the company research, fit/gap analysis, 2 project options (with draft resume bullets), and the 2 email drafts (Version A and Version B).",
        agent=agent
    )

def get_project_building_task(agent, selected_project_idea: str):
    return Task(
        description=f"Based on the chosen project idea: '{selected_project_idea}', create the Phase 0 (Scope), Phase 1 (HLD), Phase 2 (LLD), Phase 3 (Directory Structure), and Phase 4 (Diagrams in Mermaid). Output a complete design document.",
        expected_output="A comprehensive Markdown document containing the project spec, architecture design, directory tree, and mermaid diagrams.",
        agent=agent
    )

def get_resume_task(agent, company: str, job_title: str, selected_project: str, current_tex: str, feedback: str):
    return Task(
        description=f"Update the resume (in LaTeX) for Kushagra applying to {company} as {job_title}.\nThe selected project is: {selected_project}.\nHere is the current LaTeX template:\n\n{current_tex}\n\nUser feedback to apply: {feedback}\n\nPlease generate the full updated LaTeX document.",
        expected_output="The complete, compile-ready raw LaTeX code. Do NOT output markdown formatting like ```latex or any introductory text. Just the raw text that pdflatex can compile.",
        agent=agent
    )

def get_email_rewrite_task(agent, company: str, hr_email: str, job_title: str, current_email: str, feedback: str):
    return Task(
        description=f"Rewrite the cold email draft for {job_title} at {company} sending to HR email {hr_email}.\nCurrent draft:\n{current_email}\n\nUser feedback: {feedback}\n\nPlease provide the refined email.",
        expected_output="The final rewritten cold email body text, without any markdown formatting or introductory text.",
        agent=agent
    )

def run_task_1_crew(company: str, job_title: str):
    """Executes the CrewAI flow for Ideation."""
    ideator = create_ideation_agent()
    task = get_ideation_task(ideator, company, job_title)
    
    crew = Crew(
        agents=[ideator],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    result = crew.kickoff()
    return result
