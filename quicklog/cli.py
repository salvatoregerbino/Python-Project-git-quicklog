# quicklog/cli.py

import argparse  # Importazione del modulo argparse per la gestione degli argomenti da linea di comando
from typing import List  # Importazione del tipo List per la tipizzazione
from rich.console import (
    Console,
)  # Importazione della classe Console per la gestione della console
from rich.table import (
    Table,
)  # Importazione della classe Table per la creazione di tabelle

from rich.style import (
    Style,
)  # Importazione della classe Style per la gestione dello stile


# Importazioni dei moduli interni
from .models import (
    Commit,
)  # Importazione della classe Commit per la gestione dei commit
from .git_parser import (
    get_git_log_raw,
    parse_commits,
)  # Importazione della funzione parse_commits per la gestione dei commit


# Inizializza la console della libreria Rich
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

    # ----------------------
    # LOGICA DI INGRESSO
    # ----------------------


"""Definizione degli argomenti da linea di comando"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="GitQuickLog: Visualizza i commit in formato strutturato. ",
        epilog="Esempio: python -m quicklog --limit 5 --author 'Mario' --since '2025-01-01'",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Numero massimo di commit da visualizzare (default: 10)",
    )
    parser.add_argument(
        "--author",
        type=str,
        default=None,
        help="Filtro per autore o email (default: None)",
    )
    parser.add_argument(
        "--since",
        type=str,
        default=None,
        help="Filtro per i commit successivi a questa data (e.g. '2025-01-01' o '1 week ago') (default: None)",
    )
    parser.add_argument(
        "--until",
        type=str,
        default=None,
        help="Filtro per i commit precedenti a questa data (e.g. '2025-01-01' o '1 week ago') (default: None)",
    )
    parser.add_argument(
        "--grep",
        type=str,
        default=None,
        help="Filtro per i commit con messaggio contenente questa stringa (default: None)",
    )
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Filtro per i commit che hanno modificato questo percorso (default: None)",
    )

    return parser.parse_args()

    """Funzione principale di orchestrazione dell'applicazione"""


def run_app():
    # 1. Analisi degli argomenti
    args = parse_args()

    # Preparazione di un dizionario per i parametri del comando Git da passarea al parser
    filters = {
        "limit": args.limit,
        "author": args.author,
        "since": args.since,
        "until": args.until,
        "grep": args.grep,
        "path": args.path,
    }

    console.print("--- Git QuickLog:  Caricamento dei Dati ---", style="bold yellow")

    # 2. Estrazione dei dati grezzi , passando l'intero dizioanrio di filtri
    stdout, stderr = get_git_log_raw(filters=filters)

    # Controllo errori
    if stderr:
        console.print(
            f"\n[/bold red]ERRORE RILEVATO: 'Errore di sistema Git[/bold red]'\n{stderr}"
        )
        return

    # 3.Trasformazione in oggetti e Visualizzazione
    commits = parse_commits(stdout)
    display_commits(commits)
