# quicklog.py (nella directory radice)

# Rimuovi: import sys 
# Rimuovi: sys.path.insert(0, '.') 
# Lascia solo l'importazione diretta:
from quicklog.git_parser import run_git_command

def main():
    print("--- Test del Modulo Git Parser ---")
    
    stdout, stderr = run_git_command(['log', '--max-count=1'])
    
    if stderr:
        print(f"\nERRORE RILEVATO:\n{stderr}")
    else:
        print("\nComando eseguito con successo!")
        print("Output STDOUT (Ultimo Commit):\n")
        print(stdout.splitlines()[0]) 
        print("...")

if __name__ == "__main__":
    main()