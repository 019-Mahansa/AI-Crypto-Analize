import os
import sys
from datetime import date

from dotenv import load_dotenv
from rich.console import Console, Group
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

load_dotenv()

console = Console()


BANNER = r"""
  ____ ____  
 / ___||  _ \
| |    | |_) \
| |___ |  _ / 
 \____||_| \_\
"""

SUBTITLE = "AI-Powered Crypto Market Analyzer  •  BETA 2.0"

console.print()
console.print(
    Align.center(
        Panel(
            Group(
                Align.center(Text(BANNER, style="bold cyan")),
                Align.center(Text(SUBTITLE, style="italic magenta")),
                Align.center(Text(
                    f"📅  {date.today().strftime('%A, %d %B %Y')}",
                    style="dim white",
                )),
            ),
            border_style="bright_cyan",
            box=box.DOUBLE,
            padding=(1, 4),
            title="[bold yellow]✦ AI-CRYPTO-ANALYZE ✦[/bold yellow]",
            subtitle="[dim]Quantitative Trading Signals[/dim]",
        )
    )
)
console.print(Align.center(Text("━" * 60, style="dim cyan")))
console.print()


choice_text = Text()
choice_text.append("Which AI Model do you want to use?\n",
                   style="bold yellow")

models = [
    ("🤖", "OpenRouter", "Recommended", "bright_green"),
    ("🧠", "Claude",     "Recommended", "bright_green"),
    ("🐋", "DeepSeek",   "Available",   "cyan"),
    ("💬", "OpenAI",     "Coming Soon", "dim white"),
    ("✨", "Gemini",     "Available",   "cyan"),
]

left_table = Table(show_header=False, show_lines=False,
                   box=None, padding=(0, 1))
right_table = Table(show_header=False, show_lines=False,
                    box=None, padding=(0, 1))
left_table.add_column(style="bold")
left_table.add_column(style="bold")
right_table.add_column(style="bold")
right_table.add_column(style="bold")

for i, (icon, name, status, color) in enumerate(models):
    row = (f"{icon}  {i+1}. {name}", f"[{color}]{status}[/{color}]")
    if i % 2 == 0:
        left_table.add_row(*row)
    else:
        right_table.add_row(*row)

console.print(
    Align.center(
        Panel(
            Group(
                choice_text,
                Columns(
                    [Align.left(left_table),
                     Align.left(right_table)],
                    equal=True, expand=True, align="center",
                ),
            ),
            border_style="bright_magenta",
            box=box.ROUNDED,
            padding=(1, 2),
            title="[bold white]⚡ AI MODEL SELECTION ⚡[/bold white]",
        )
    )
)
console.print()

pick = str(input("👉 Pick yours : ")).lower().strip()
print(pick)

console.print(
    Align.left(
        Panel(
            f"[bold cyan]You selected:[/bold cyan] "
            f"[bold yellow]{pick.upper()}[/bold yellow]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(0, 2),
            width=60,
        )
    )
)
console.print()


if pick in ("openrouter", "1"):
    from ai.openRouter import jalankan_openrouter
    print(jalankan_openrouter())

elif pick in ("claude", "2"):
    console.print(Panel(
        "[bold red]⚠  Sorry, the Claude model is still under "
        "development.[/bold red]",
        border_style="red", box=box.ROUNDED))

elif pick in ("deepseek", "3"):
    from ai.deepseek import jalankan_openrouter
    console.print(Panel(
        "[bold cyan]===== Please wait, your AI is working right "
        "now! =====[/bold cyan]",
        border_style="cyan", box=box.ROUNDED))
    print(jalankan_openrouter())

elif pick in ("openai", "4"):
    console.print(Panel(
        "[bold red]⚠  Sorry, the OpenAI model is still under "
        "development.[/bold red]",
        border_style="red", box=box.ROUNDED))

elif pick in ("gemini", "5"):
    from ai.gemini import jalankan_gemini
    console.print(Panel(
        "[bold cyan]===== Please wait, your AI is working right "
        "now! =====[/bold cyan]",
        border_style="cyan", box=box.ROUNDED))
    print(jalankan_gemini())

else:
    console.print(Panel(
        "[bold red]❌  Your input is invalid, please try again!"
        "[/bold red]",
        border_style="red", box=box.ROUNDED))

console.print()
console.print(
    Align.center(
        Text("✦ Thank you for using AI-Crypto-Analize ✦",
             style="bold magenta")
    )
)
