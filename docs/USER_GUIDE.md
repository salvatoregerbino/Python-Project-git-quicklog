# 📖 Git QuickLog - Guida Utente Completa

Benvenuto nel manuale ufficiale di **Git QuickLog**.
Questa guida ti accompagnerà dall'installazione all'uso avanzato dei filtri per analizzare i tuoi repository.

---

## 📋 Indice
1. [Introduzione](#introduzione)
2. [Installazione e Configurazione](#installazione)
3. [Comandi Base](#comandi-base)
4. [Filtri Avanzati](#filtri-avanzati)
5. [Visualizzazione Dettagli (Diff)](#diff-view)
6. [Esempi di Utilizzo Reale](#esempi)
7. [Risoluzione Problemi (Troubleshooting)](#troubleshooting)

---

## <a name="introduzione"></a>1. Introduzione

**Git QuickLog** è un wrapper per Git che migliora l'esperienza di lettura dei log.
Invece di stampare testo grezzo, QuickLog analizza l'output di Git e costruisce una
 **TUI (Text User Interface)** interattiva utilizzando la libreria `Rich`.

**Caratteristiche Chiave:**
* 🎨 **Output Colorato:** Distingue visivamente autori, date e hash.
* 📊 **Tabellare:** Colonne allineate per una scansione rapida.
* **Smart Filters:** Non serve conoscere Regex complesse.

---

## <a name="installazione"></a>2. Installazione e Configurazione

### Prerequisiti
* Python 3.9 o superiore.
* Git installato e accessibile da terminale.

### Metodo 1: Installazione Standard (Raccomandata)
Per utilizzare il tool come comando globale nel tuo ambiente virtuale:

```bash
pip install .
```

### Metodo 2: Installazione Sviluppatore (Editable)
Se intendi modificare il codice sorgente di QuickLog e vedere le modifiche in tempo reale senza reinstallare ogni volta:

```Bash
pip install -e .
```

> **💡 Consiglio:** È buona norma installare il tool all'interno di un ambiente virtuale (`venv`) per non "sporcare" l'installazione globale di Python.

---

## <a name="3-primo-utilizzo"></a>3. Primo Utilizzo

Una volta installato, il comando `quicklog` è disponibile globalmente.
Per usarlo, apri il terminale e **spostati in una cartella che sia un repository Git**.

### Comando Base
Mostra gli ultimi 10 commit del branch corrente:

```bash
quicklog
```
## Menu di Aiuto
Visualizza la lista interattiva di tutti i comandi disponibili:

```bash
quicklog --help
```
## <a name="4-guida-ai-filtri-avanzati"></a>4. Guida ai Filtri Avanzati

QuickLog brilla quando devi cercare qualcosa di specifico. Puoi combinare più filtri insieme per restringere la ricerca.

### Tabella Riferimento Comandi

| Opzione           | Descrizione                                             | Esempio             |
| :---------------- | :------------------------------------------------------ | :------------------ |
| `--limit <N>`     | Imposta il numero massimo di righe visualizzate.        | `quicklog --limit 50` |
| `--author "<Nome>"` | Filtra per nome o email dell'autore.                    | `quicklog --author "Mario"` |
| `--grep "<Testo>"` | Cerca una parola o frase nel messaggio del commit.      | `quicklog --grep "fix bug"` |
| `--path "<File>"` | Mostra solo i commit che hanno modificato un file specifico. | `quicklog --path "src/main.py"` |
| `--since "<Data>"` | Mostra commit successivi a una data.                    | `quicklog --since "2024-01-01"` |
| `--until "<Data>"` | Mostra commit precedenti a una data.                    | `quicklog --until "1 week ago"` |

### Esempi Pratici

#### Scenario 1: Cosa ha fatto Mario la settimana scorsa?

```bash
quicklog --author "Mario" --since "1 week ago"
```

#### Scenario 2: Quando abbiamo modificato il file README l'ultima volta?

```bash
quicklog --path "README.md" --limit 5
```

#### Scenario 3: Cerca tutti i commit che parlano di "Refactoring"

```bash
quicklog --grep "refactor"
```

## <a name="5-visualizzazione-dettagli-diff-view"></a>5. Visualizzazione Dettagli (Diff View)

Oltre alla lista, QuickLog permette di esaminare il codice modificato in un commit specifico.

Esegui `quicklog` per trovare l'Hash Breve (es. `a1b2c3d`) nella prima colonna.

Lancia il comando con l'opzione `--show`:

```bash
quicklog --show a1b2c3d
```

Cosa vedrai: Il terminale mostrerà le differenze ("Diff") con evidenziazione della sintassi:

*   🟢 Verde (`+`): Righe aggiunte.
*   🔴 Rosso (`-`): Righe rimosse.

## <a name="6-risoluzione-problemi-troubleshooting"></a>6. Risoluzione Problemi (Troubleshooting)

### Errore: `quicklog: command not found`

Causa: La cartella degli script di Python non è nel `PATH` del sistema.
Soluzione:

1.  Assicurati di aver attivato l'ambiente virtuale (`source .venv/bin/activate`).
2.  Oppure, aggiungi la cartella `Scripts` di Python alle variabili d'ambiente.

### Errore: `fatal: not a git repository`

Causa: Stai eseguendo il comando in una cartella normale, non in un repository Git.
Soluzione: Spostati in una cartella dove hai inizializzato git (`git init`) o clonato un progetto.

### La tabella si vede male o i colori sono strani

Causa: Il tuo terminale potrebbe non supportare i colori `TrueColor`.
Soluzione: Prova ad usare un terminale moderno come Windows Terminal, Git Bash o iTerm2. QuickLog adatta automaticamente i colori, ma richiede un terminale standard ANSI.