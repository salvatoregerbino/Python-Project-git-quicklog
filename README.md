# Git QuickLog

**Git QuickLog** è un tool CLI (Command Line Interface) avanzato scritto in Python per esplorare la cronologia dei repository Git.

A differenza del comando nativo `git log`, QuickLog offre un'interfaccia **colorata**, **tabellare** e **altamente leggibile**, pensata per sviluppatori che vogliono analizzare rapidamente il proprio codice senza ricordare comandi complessi.

![Screenshot](https://via.placeholder.com/800x400?text=Anteprima+Git+QuickLog)
*(Qui potrai inserire uno screenshot del tuo terminale)*

## Funzionalità Principali

*  **Interfaccia TUI:** Visualizzazione pulita con tabelle e colori (grazie alla libreria `rich`).
*  **Filtri Avanzati:** Filtra per Autore, Data, Messaggio (Grep) e Percorso file.
*  **Diff Viewer:** Visualizza le differenze di codice con syntax highlighting direttamente nel terminale (`--show`).
* **Cross-Platform:** Funziona perfettamente su GNU/Linux, Windows e macOS.

## 📦 Installazione

### Prerequisiti
* Python 3.9 o superiore [https://www.python.org/downloads/](https://www.python.org/downloads/)
* Git installato nel sistema [https://git-scm.com/downloads](https://git-scm.com/downloads)

### Installazione Rapida
1.  Clona il repository:
    ```bash
    git clone [https://github.com/TUO-USERNAME/git-quicklog.git](https://github.com/TUO-USERNAME/git-quicklog.git)
    cd git-quicklog
    ```

2.  Installa il tool nel sistema:
    ```bash
    pip install .
    ```

## Utilizzo

Una volta installato, puoi digitare `quicklog` in **qualsiasi cartella** del tuo computer.

### Comandi Base
```bash
# Visualizza gli ultimi 10 commit
quicklog

# Visualizza il menu di aiuto grafico
quicklog --help

