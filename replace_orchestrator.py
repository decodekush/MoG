import re

with open('src/orchestrator.py', 'r') as f:
    content = f.read()

# Replace imports
content = content.replace("from rich.console import Console\nfrom rich.markdown import Markdown\nimport questionary", "from rich.markdown import Markdown\nfrom src.ui import console, ask_text, ask_select, print_step, print_success, print_error, status, get_claude_style")

# Remove redundant console/style init
content = content.replace("console = Console()\n", "")
content = content.replace("    from src.cli import get_claude_style\n    style = get_claude_style()\n", "    style = get_claude_style()\n")

# Replace console prints
content = content.replace('console.print(f"[dim]❯ Extracting skills from {company} / {job_title} / {email}...[/dim]")', 'print_step(f"Extracting skills from {company} / {job_title}...")')

content = re.sub(r'console\.print\("\[dim\]❯ Ideator Agent analyzing gaps\.\.\.\[/dim\]"\)', 'print_step("Ideator Agent analyzing gaps...")', content)

content = re.sub(r'console\.print\("\[bold\]Resume Generation\[/bold\]"\)\n\s+console\.print\("\[dim\]❯ Initializing Resume Agent\.\.\.\[/dim\]"\)', 'console.print("\\n[bold]Resume Generation[/bold]")\n    print_step("Initializing Resume Agent...")', content)

content = re.sub(r'console\.print\("\[dim\]❯ Drafting initial outreach email\.\.\.\[/dim\]"\)', 'print_step("Drafting initial outreach email...")', content)

# Spinners
content = content.replace('print_step("Ideator Agent analyzing gaps...")\n    if MOCK_MODE:\n        time.sleep(1)', 'with status("Ideator Agent analyzing gaps..."): \n        if MOCK_MODE:\n            time.sleep(1)')

# MOCK_MODE waits
content = re.sub(r'if MOCK_MODE:\n\s+time\.sleep\(\d+\)', lambda m: m.group(0), content) # Keep logic but just replacing prints with status

# Actually it's easier to manually edit the chunks or write a complete file since I know what it needs to look like.
# Let's read orchestrator.py line by line and adjust it.
