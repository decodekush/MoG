import re

with open('src/orchestrator.py', 'r') as f:
    content = f.read()

# Fix multi-line questionary.select
content = re.sub(
    r'action = questionary\.select\([\s\S]*?choices=\[([\s\S]*?)\],\s*style=style\s*\)\.ask\(\)',
    r'action = ask_select("❯ Email drafted. What would you like to do?", choices=[\1])',
    content
)

# Fix remaining console prints
content = content.replace("console.print(\"[yellow]No data found in the spreadsheet.[/yellow]\")", "print_error(\"No data found in the spreadsheet.\")")
content = content.replace("console.print(f\"[bold magenta]Found {len(jobs_to_queue)} jobs marked as 'Not Applied'.[/bold magenta]\")", "print_step(f\"Found {len(jobs_to_queue)} jobs marked as 'Not Applied'.\")")
content = content.replace("console.print(\"Run [bold cyan]mog[/bold cyan] and select 'Review Dashboard' to process the queue.\")", "print_step(\"Run mog and select 'Review Dashboard' to process the queue.\")")

# Fix `print_step("Checking Google Sheets for pending applications...[/cyan]")`
content = content.replace("print_step(\"Checking Google Sheets for pending applications...[/cyan]\")", "print_step(\"Checking Google Sheets for pending applications...\")")

with open('src/orchestrator.py', 'w') as f:
    f.write(content)
