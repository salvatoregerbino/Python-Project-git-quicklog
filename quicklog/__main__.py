# quicklog/__main__.py
from .git_parser import get_git_log_raw, parse_commits  # Importazione del modulo parser
from .cli import display_commits  # Importazione del modulo cli


def main():
    print("--- Git QuickLog:  Caricamento dei Dati ---")

    stdout, stderr = get_git_log_raw(limit=10)

    # 1. Importazione dei dati grezzi con il formato speciale pensato
    if stderr:
        print(f"\nERRORE RILEVATO:\n{stderr}")
        return

    # 2. Trasformare il text in objects
    commits = parse_commits(stdout)

    # 3.Visualizzazione del risultato usando il modulo CLI
    display_commits(commits)


if __name__ == "__main__":
    main()
