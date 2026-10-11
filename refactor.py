import re

with open('src/orchestrator.py', 'r') as f:
    content = f.read()

# Replace imports
content = content.replace("from rich.console import Console", "from src.ui import console, ask_text, ask_select, print_step, print_success, print_error, status")
content = content.replace("console = Console()", "")
content = content.replace("from rich.prompt import Confirm, Prompt\n", "")

# Remove get_claude_style because ui handles it
content = re.sub(r'    from src\.cli import get_claude_style\n    style = get_claude_style\(\)\n', '', content)

# Replace console.print("[dim]❯ ...[/dim]") with print_step("...")
content = re.sub(r'console\.print\(\[?"f?"?\'?\[dim\]❯ (.+?)\[/dim\]\'?"?\]?\)', lambda m: f'print_step("{m.group(1)}")', content)
content = re.sub(r'console\.print\(f"\[dim\]❯ (.+?)\[/dim\]"\)', lambda m: f'print_step(f"{m.group(1)}")', content)
content = re.sub(r'console\.print\("\[dim\]❯ (.+?)\[/dim\]"\)', lambda m: f'print_step("{m.group(1)}")', content)

# Replace print("[dim]✓ ...[/dim]")
content = re.sub(r'console\.print\(f"\[dim\]✓ (.+?)\[/dim\]"\)', lambda m: f'print_success(f"{m.group(1)}")', content)
content = re.sub(r'console\.print\("\[dim\]✓ (.+?)\[/dim\]"\)', lambda m: f'print_success("{m.group(1)}")', content)

# Replace print("[green]...[/green]")
content = re.sub(r'console\.print\(f"\[green\](.+?)\[/green\]"\)', lambda m: f'print_success(f"{m.group(1)}")', content)
content = re.sub(r'console\.print\("\[green\](.+?)\[/green\]"\)', lambda m: f'print_success("{m.group(1)}")', content)

# Replace print("[red]...[/red]")
content = re.sub(r'console\.print\(f"\[red\](.+?)\[/red\]"\)', lambda m: f'print_error(f"{m.group(1)}")', content)
content = re.sub(r'console\.print\("\[red\](.+?)\[/red\]"\)', lambda m: f'print_error("{m.group(1)}")', content)

# Replace questionary selects
content = re.sub(r'questionary\.select\(\s*"(.+?)",\s*choices=\[(.*?)\],\s*style=style\s*\)\.ask\(\)', lambda m: f'ask_select("{m.group(1)}", choices=[{m.group(2)}])', content)

# Replace questionary text
content = re.sub(r'questionary\.text\(\s*"(.+?)",\s*style=style\s*\)\.ask\(\)', lambda m: f'ask_text("{m.group(1)}")', content)

# Update run_task_2 specific ones
content = content.replace('console.print("- Scraping', 'print_step("Scraping')
content = content.replace('console.print("\\n[cyan]Checking', 'print_step("Checking')

with open('src/orchestrator.py', 'w') as f:
    f.write(content)
