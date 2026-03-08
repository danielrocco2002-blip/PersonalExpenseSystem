# Sistema di Gestione delle spese personali e del budget
## Struttura del repository

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

## Schema del database

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

## Istruzioni di avvio

### 1. Clonarea il repository

```bash
git clone https://github.com/nomeutente/PersonalExpenseSystem.git
cd PersonalExpenseSystem
```

### 2. Inizializzare il database (solo la prima volta)

```bash
python src/init_db.py
```

### 3. Avviare il programma

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

