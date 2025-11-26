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


from rich.syntax import (
    Syntax,
)  # Importazione della classe Syntax per la gestione del syntax highlighting


from rich.panel import (
    Panel,
)  # Importazione della classe


# Importazioni dei moduli interni
from .models import (
    Commit,
)  # Importazione della classe Commit per la gestione dei commit
from .git_parser import (
    get_git_log_raw,
    parse_commits,
    get_commit_diff,
)  # Importazione della funzione parse_commits per la gestione dei commit


# Inizializza la console della libreria Rich
console = Console()

# --- 1. FUNZIONE HELP PERSONALIZZATA (VIEW) ---


def print_help():
    """
    Renderizza una guida interattiva sostituendo quella di default.
    """

    # Intestazione con Panel
    console.print(
        Panel.fit(
            "[bold cyan]Git QuickLog - Manuale Utente[/bold cyan]", border_style="cyan"
        )
    )
    console.print(
        "Un tool CLI avanzato per esplorare la storia di Git con stile.\n",
        style="italic dim",
    )

    # Tabella dei Comandi
    table = Table(
        title="Lista Comandi e Opzioni",
        header_style="bold magenta",
        border_style="cyan",
    )

    table.add_column("Opzione", style="bold green", justify="left")
    table.add_column("Descrizione", style="white")
    table.add_column("Esempio", style="dim cyan")

    # Definizione righe (Documentazione)
    table.add_row("-h, --help", "Mostra questa schermata di aiuto", "")
    table.add_row(
        "--limit <N>", "Numero di commit da mostrare (Default: 10)", "--limit 5"
    )
    table.add_section()  # Linea separatrice

    table.add_row(
        "--author <nome>", "Filtra per nome o email autore", "--author 'Mario'"
    )
    table.add_row("--grep <testo>", "Cerca testo nel messaggio", "--grep 'fix'")
    table.add_section()

    table.add_row(
        "--since <data>", "Commit successivi alla data", "--since '2023-01-01'"
    )
    table.add_row(
        "--until <data>", "Commit precedenti alla data", "--until '1 week ago'"
    )
    table.add_row("--path <file>", "Filtra per file/percorso", "--path 'main.py'")
    table.add_section()

    table.add_row("--show <hash>", "Mostra il DIFF colorato", "--show a1b2c3d")

    console.print(table)

    console.print("\n[bold yellow]Esempio Completo:[/bold yellow]")
    console.print(
        "  python -m quicklog --limit 5 --author 'Salvatore' --grep 'feat'",
        style="on black bold white",
    )
    print()  # Spaziatura finale


# --- 2. FUNZIONI DI VISUALIZZAZIONE DATI (Esistenti) ---
def display_commits(commits: List[Commit]):
    """Stampa una lista di commit in formato tabellare utilizzando la libreria Rich."""
    if not commits:
        console.print(
            "[yellow]Nessun commit trovato nella repository corrente.", style="warning"
        )
        return

    # -- Creazione della tabella Rich ---
    table = Table(
        title="Risultati Ricerca",
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
    # Visualizzazione del diff
    # ----------------------


def display_diff(commit_hash: str, diff_text: str):
    """Visualizza il diff di un commit specifico usando la sintassi di syntax highlighting."""
    console.print(
        f"\n--- Dettaglio del commit {commit_hash} ---\n", style="bold yellow"
    )

    # Creazione di un oggetto Syntax per la libreria Rich
    # Questa libreria permette di evidenziare le differenze tra i file come in un editor di codice
    syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=True)
    console.print(syntax)

    # ----------------------
    # LOGICA DI INGRESSO
    # ----------------------


"""Definizione degli argomenti da linea di comando"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="GitQuickLog: Visualizza i commit in formato strutturato. ",
        add_help=False,
    )

    parser.add_argument(
        "-h", "--help", action="store_true", help="Mostra aiuto personalizzato"
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
    parser.add_argument(
        "--show",
        type=str,
        default=None,
        help="Mostra il dettaglio (diff) di uno specifico commit dato il suo hash",
    )

    return parser.parse_args()

    """Funzione principale di orchestrazione dell'applicazione"""


# --- MODALITA' 1: VISUALIZZAZIONE DETTAGLIO (--show) ---


def run_app():
    # 1. Analisi degli argomenti
    args = parse_args()

    # --- BRANCH 1: HELP PERSONALIZZATO ---
    if args.help:
        print_help()  # Chiamata alla nuova funzione grafica
        return  # Interrompe l'esecuzione qui

    # --- BRANCH 2: MODALITA' SHOW (Diff) ---

    if args.show:
        # Se l'utente ha chiesto di vedere il diff di un commit specifico , la funzione fa solo quello e si ferma
        stdout, stderr = get_commit_diff(args.show)

        # Controllo errori
        if stderr:
            console.print(
                f"[/bold red]ERRORE RILEVATO:[/bold red] Commit '{args.show}' non trovato."
            )
            return

        display_diff(args.show, stdout)
        return

    # --- MODALITA' 3: VISUALIZZAZIONE TABELLA (DEFAULT)---

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

    # Estrazione dei dati grezzi , passando l'intero dizioanrio di filtri
    stdout, stderr = get_git_log_raw(filters=filters)

    # Controllo errori
    if stderr:
        console.print(
            f"\n[/bold red]ERRORE RILEVATO: 'Errore di sistema Git[/bold red]'\n{stderr}"
        )
        return
    # Trasformazione in oggetti e Visualizzazione
    commits = parse_commits(stdout)
    display_commits(commits)
