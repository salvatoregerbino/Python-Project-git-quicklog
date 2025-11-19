#quicklog/git-parser.py

import subprocess
import shlex
from typing import List,Tuple, Optional
from .models import Commit

#--- 1.Funzione di Utility Principale ---

"""
La seguente funzione esegue un comando Git e cattura l'output standard e gli errori.

Args:
     args: Una lista di stringhe che rappresentano il comando Git e i suoi argoementi.
          Esempio: ['log', '--max-count=5']

Returns:
    Una tupla contenente (stdout_output, stderr_output).
    Restituisce None se un output non è presente.
"""

def run_git_command(args: List[str]) -> Tuple[Optional[str], Optional[str]]:
# Prepara il comando completo (il primo elemento sempre 'git')
   full_command =['git']  + args

#--- Spiegazione dei parametri di subprocess.run ---
   try:
      # 1. full_command: La lsita di stringhe del commando 
      # 2. capture_output=True: Cattura stdout e stderr separatamente 
      # 3. text=True: Decodifica l'output come stringa (usando l'encoding di default)
      # 4. encoding='utf-8': Assicure che i char speciali e nomi dei file vengano getstiti correttamente 
      result = subprocess.run(
         full_command,
         capture_output=True,
         text=True,
         encoding='utf-8',
         check=False      # Non sollevare un'eccezione Python per codici di uscita != 0  
      )

      stdout = result.stdout.strip() if result.stdout else None
      stderr = result.stderr.strip() if result.stderr else None

      return stdout,stderr
   
   except FileNotFoundError:
      # Cattura l'errore se 'git' non è un comando riconosciuto (Se Git non istallato o non nel PATH)
     return None, "Errore: Git non è installato o non è presente nel tuo PATH di Sistema."
   
# --- 2. Funzione specifica per il Log ---

"""
Ottiene la cronologia di Git in un formato RAW personalizzato.

Args:
    format_string: Il formato di output personalizzaato di Git.

Returns: 
Una tupla contenente (output_grezzo, messaggio_di_errore).
"""
def get_git_log_raw(format_string: str) -> Tuple[Optional[str], Optional[str]]:
   
   #Questo è il comando Git fondamentalae per il recuper di dati che ho deciso di utilzzare.
   # Utilizzo '--pretty=format:' per un output pulito, faacile daa analaizzare (parsing):
    logs_args = ['log', f'--pretty=format:{format_string}', '--all']

    #Esegue il comaando traamite la funzione utlity
    return run_git_command(logs_args)

def get_git_log_raw(limit: int = 10) -> Tuple[Optional[str], Optional[str]]:
   # Definiamo un formato personalizzato per Git:
   # %h = hash breve, %H = hash full, %an = nome autore, %ae = email, %at = timestamp, %s = messaggio
   # Usiamo '|' come separatore perché è raaro nei mex commit.

   fmt = "%h|%H|%an|%se|%at|%s"

   args = ['log', f'--pretty=format:{fmt}',f'-n{limit}']
   return run_git_command(args)


"""Trasforma la stringa grezza di output di Git in una lista di oggetti Commiit"""

def parse_commits(raw_output: str) -> List[Commit]:

   commits = []

   if not raw_output:
      return commits
   
   # Divide le righe . Ogni riga è un commit (grazie all'integrazione del formato che utilizzo)
   lines = raw_output.strip().split('\n')

   for line in lines:
      # Esempio di riga grezza che il sistema si aspetterebbe
      # "hash_breve|hash_full|autore|email|timestamp|messaggio"
       parts = line.split('|')

       if len(parts) >= 6:
          #Creazione di un object 'Commit' "spacchettando" i pezzi 
          c = Commit(
            hash_short=parts[0],
            hash_full=parts[1],
            author_name=parts[2],
            author_email=[3],
            timestamp=int(parts[4]),
            message=parts[5]
          )
          commits.append(c)
   return commits