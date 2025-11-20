# quicklog/cli.py

from typing import List
from rich.console import Console
from rich.table import Table
from rich.style import Style
from .models import Commit

# Inizializza la console
console = Console()


def display_commits(commits: List[Commit]):
    """Stampa una lista di commit in formato tabellare utilizzando la libreria Rich."""
    if not commits:
        console.print(
            "[yellow]Nessun commit trovato nella repository corrente.", style="warning"
        )
        return

    # -- Creazione della tabella Rich ---
    table = Table(
        title="Git QuickLog",
        style=Style(color="cyan"),
        show_header=True,
        header_style="bold magenta",
    )

    # -- Aggiunta delle colonne alla tabella ---
    table.add_column("Hash Breve", style="dim", justify="left")
    table.add_column("Autore", style="blue")
    table.add_column("Data", style="green", justify="center")
    table.add_column("Messaggio", justify="center", overflow="fold")

    # -- Aggiunta dei commit alla tabella ---
    for commit in commits:
        table.add_row(
            commit.hash_short,
            commit.author_name,
            commit.date_str,
            commit.message,
            end_section=(
                True if commit == commits[0] else False
            ),  # Stacca il primo per evidenziarlo
        )

    # Stampa la tabella sulla console
    console.print(table)
