# quicklog/__main__.py
import argparse  # Importazione del modulo argparse per la gestione degli argomenti da linea di comando
from .git_parser import get_git_log_raw, parse_commits  # Importazione del modulo parser
from .cli import display_commits  # Importazione del modulo cli

"""Definizione degli argomenti da linea di comando"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="GitQuickLog: Visualizza i commit in formato strutturato. ",
        epilog="Esempio: python -m quicklog --limit 5",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Numero massimo di commit da visualizzare (default: 10)",
    )
    return parser.parse_args()


def main():
    # 1. Analisi degli argomenti
    args = parse_args()
    limit = args.limit  # Estrazione del limite desiderato dagli argomenti

    print("--- Git QuickLog:  Caricamento dei Dati ---")

    # 2. Estrazione dei dati grezzi
    stdout, stderr = get_git_log_raw(limit=limit)

    # Controllo errori
    if stderr:
        print(f"\nERRORE RILEVATO:\n{stderr}")
        return

    # 3.Trasformazione in oggetti e Visualizzazione
    commits = parse_commits(stdout)
    display_commits(commits)


if __name__ == "__main__":
    main()
