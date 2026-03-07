# Sistema di Gestione delle spese personali e del budget

Sistema console per la gestione delle spese personali con database SQLite.

## Struttura del Repository

```
PersonalExpenseSystem/
├── src/
│   ├── main.py        # Applicazione principale
│   └── init_db.py     # Script di inizializzazione database
├── sql/
│   └── database.sql   # Script SQL (DDL + dati di esempio + query)
├── demo/
│   └── demo_video.mp4 # Video dimostrativo
└── README.md
```

## Schema Logico del Database

```
┌─────────────────┐         ┌──────────────────────────────┐
│   CATEGORIE     │         │           SPESE              │
├─────────────────┤         ├──────────────────────────────┤
│ id   PK  INT    │◄────────│ id           PK  INT         │
│ nome UQ  TEXT   │    1:N  │ data             TEXT NOT NULL│
│      NOT NULL   │         │ importo          REAL >0     │
└─────────────────┘         │ categoria_id  FK INT         │
         ▲                  │ descrizione      TEXT        │
         │                  └──────────────────────────────┘
         │ 1:N
┌─────────────────────────────┐
│           BUDGET            │
├─────────────────────────────┤
│ id           PK  INT        │
│ mese             TEXT       │
│ categoria_id  FK INT        │
│ importo          REAL >0    │
│ UNIQUE(mese, categoria_id)  │
└─────────────────────────────┘
```

### Vincoli di Integrità Presenti nel Codice SQL

| Vincolo       | Tabella     | Campo / Descrizione                          |
|---------------|-------------|----------------------------------------------|
| `PRIMARY KEY` | tutte       | campo `id` AUTOINCREMENT                     |
| `FOREIGN KEY` | spese       | `categoria_id` → categorie(id)               |
| `FOREIGN KEY` | budget      | `categoria_id` → categorie(id)               |
| `CHECK`       | spese       | `importo > 0`                                |
| `CHECK`       | budget      | `importo > 0`                                |
| `UNIQUE`      | categorie   | `nome`                                       |
| `UNIQUE`      | budget      | coppia `(mese, categoria_id)`                |
| `NOT NULL`    | tutte       | campi obbligatori (nome, data, importo, ...) |

## Requisiti per l'Esecuzione

- **Python 3.8+** (incluso nella maggior parte dei sistemi operativi moderni)
- Nessuna libreria esterna richiesta — si usa solo `sqlite3` dalla libreria standard

## Istruzioni di Avvio

### 1. Clona il repository

```bash
git clone https://github.com/nomeutente/PersonalExpenseSystem.git
cd PersonalExpenseSystem
```

### 2. Inizializza il database (solo la prima volta)

```bash
python src/init_db.py
```

Questo comando crea il file `sql/spese.db` e inserisce le categorie, spese e budget di esempio.

### 3. Avvia il programma

```bash
python src/main.py
```

## Funzionalità

| Voce menu | Descrizione |
|-----------|-------------|
| 1. Gestione Categorie | Aggiunge nuove categorie di spesa |
| 2. Inserisci Spesa    | Registra una spesa con data, importo e categoria |
| 3. Definisci Budget   | Imposta o aggiorna un budget mensile per categoria |
| 4. Visualizza Report  | Sottomenu con 3 tipologie di report |
| 5. Esci               | Chiude l'applicazione |

## Esempi d'Uso

```
-------------------------
 SISTEMA SPESE PERSONALI
-------------------------
1. Gestione Categorie
2. Inserisci Spesa
3. Definisci Budget Mensile
4. Visualizza Report
5. Esci
-------------------------
Inserisci la tua scelta: 2

--- INSERISCI SPESA ---
Data (YYYY-MM-DD): 2025-03-01
Importo: 45.50
Nome categoria: Alimentari
Descrizione (facoltativa): Spesa weekend
Spesa inserita correttamente.
```
