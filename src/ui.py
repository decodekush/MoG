import sys
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()

def get_claude_style():
    return questionary.Style([
        ('qmark', 'fg:#888888'),
        ('question', 'bold'),
        ('answer', 'fg:#cccccc'),
        ('pointer', 'fg:#10b981 bold'),
        ('highlighted', 'fg:#ffffff bold'),
        ('selected', 'fg:#ffffff'),
        ('separator', 'fg:#555555'),
        ('instruction', 'fg:#666666'),
        ('text', ''),
    ])

def handle_cancel(result):
    if result is None:
        console.print("\n[dim]Cancelled by user.[/dim]")
        sys.exit(0)
    return result

GREEN = "\033[32m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

BANNER = f"""{GREEN}{BOLD}
 ███╗   ███╗ ██████╗  ██████╗ 
 ████╗ ████║██╔═══██╗██╔════╝ 
 ██╔████╔██║██║   ██║██║  ███╗
 ██║╚██╔╝██║██║   ██║██║   ██║
 ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝
 ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ 
{RESET}{DIM} ⚡ Automated Job Application CLI{RESET}
"""

def print_header():
    console.clear()
    print(BANNER)

def ask_text(message: str) -> str:
    return handle_cancel(questionary.text(message, style=get_claude_style(), qmark="❯").ask())

def ask_select(message: str, choices: list, instruction: str = "↑↓ Navigate · Enter Select · Esc Cancel") -> str:
    return handle_cancel(questionary.select(
        message,
        choices=choices,
        style=get_claude_style(),
        qmark="❯" if message else "",
        pointer="❯",
        instruction=instruction
    ).ask())

def ask_confirm(message: str, default: bool = True) -> bool:
    result = questionary.confirm(message, default=default, style=get_claude_style(), qmark="❯").ask()
    if result is None:
        console.print("\n[dim]Cancelled by user.[/dim]")
        sys.exit(0)
    return result

def print_step(message: str):
    console.print(f"[dim]○ {message}[/dim]")

def print_success(message: str):
    console.print(f"[green]✓[/green] {message}")

def print_error(message: str):
    console.print(f"[red]✗[/red] {message}")

def status(message: str):
    return console.status(f"[bold]{message}[/bold]", spinner="dots")
