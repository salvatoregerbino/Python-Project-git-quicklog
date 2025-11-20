# quicklog/__main__.py
import argparse  # Importazione del modulo argparse per la gestione degli argomenti da linea di comando
from .git_parser import get_git_log_raw, parse_commits  # Importazione del modulo parser
from .cli import display_commits  # Importazione del modulo cli

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
    return parser.parse_args()


def main():
    # 1. Analisi degli argomenti
    args = parse_args()

    # Preparazione di un dizionario per i parametri del comando Git da passarea al parser
    filter = {
        "limit": args.limit,
        "author": args.author,
        "since": args.since,
        "until": args.until,
    }

    print("--- Git QuickLog:  Caricamento dei Dati ---")

    # 2. Estrazione dei dati grezzi , passando l'intero dizioanrio di filtri
    stdout, stderr = get_git_log_raw(filters=filter)

    # Controllo errori
    if stderr:
        print(f"\nERRORE RILEVATO:\n{stderr}")
        return

    # 3.Trasformazione in oggetti e Visualizzazione
    commits = parse_commits(stdout)
    display_commits(commits)


if __name__ == "__main__":
    main()
