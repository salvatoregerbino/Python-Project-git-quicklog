#
from .git_parser import get_git_log_raw, parse_commits #Impo

def main():
    print("--- Git QuickLog:  Test Modelli ---")
    
    stdout, stderr = get_git_log_raw(limit=5)
    
    # 1. Importazione dei dati grezzi con il formato speciale pensato
    if stderr:
        print(f"\nERRORE RILEVATO:\n{stderr}")
        return
    
    # 2. Trasformare il text in objects
    commits = parse_commits(stdout)

    # 3. Stampa i riusltati usando la property dell'object 

    print(f"Trovati {len(commits)} commit:\n")
    
    for commit in commits:
        # Uso di .hash_short e .date_str definit nel models
        print(f"[{commit.date_str}] {commit.hash_short} - {commit.author_name}")
        print(f"   Messaggio: {commit.message}")
        print("-" * 40)
        

if __name__ == "__main__":
    main()