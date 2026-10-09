# EMQ (Automated Job Application CLI)

**EMQ** is a fully automated, interactive Command-Line Interface (CLI) tool designed to streamline the tech job application process. It acts as an autonomous agent that researches a company, builds tailored projects, generates ATS-optimized LaTeX resumes (compiled to PDF), drafts personalized cold emails, and sends them via Gmail—all while allowing human-in-the-loop review and feedback.

## Features

- **`emq apply`**: Manual Mode. Interactively applies to a single job. It will research the company, propose tailored projects, build the codebase, draft a custom resume, and prepare a cold email for you to review and refine.
- **`emq auto`**: Automated Mode. Scrapes job boards (YC, Career pages) and syncs them to a Google Sheet. It then queues "Not Applied" jobs for background processing.
- **`emq review`**: Approval Dashboard. Review queued applications and approve the generated resumes and emails before sending them out in bulk.

## Prerequisites

- Python 3.10+
- MacTeX / BasicTeX (for compiling `.tex` resumes to `.pdf`)
- A Google Cloud Project with **Gmail API** and **Google Sheets API** enabled.
- A Gemini API key.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/decodekush/MoG.git
   cd MoG
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

3. Set up your environment variables:
   ```bash
   cp .env.example .env
   ```
   Add your `GEMINI_API_KEY` and `GOOGLE_SHEETS_ID` to the `.env` file.

4. Add your Google OAuth credentials:
   Place your `credentials.json` file in the root directory. (See `setup.md` for detailed instructions on obtaining this).

## Usage

Once installed, you can use the `emq` command globally (as long as your virtual environment is active, or if you've symlinked the executable to your `~/.local/bin` folder).

```bash
# Start a manual application process
emq apply

# Scan for jobs and queue them
emq auto

# Review pending applications
emq review
```

## Architecture

EMQ uses **CrewAI** to orchestrate several specialized agents:
- **Project Ideator Agent:** Researches the company and proposes tailored project ideas.
- **Project Builder Agent:** Writes the code/repository structure for the chosen project.
- **Resume & Email Agent:** Updates your LaTeX resume with new bullet points matching the job description and project, compiles it to PDF via `pdflatex`, and drafts the cold email.

## License

MIT
