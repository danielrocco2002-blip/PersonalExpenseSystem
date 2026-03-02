"""
Inizializza il database SQLite eseguendo database.sql.
Esegui questo script una sola volta prima di avviare main.py.
"""
import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
SQL_PATH  = os.path.join(BASE_DIR, '..', 'sql', 'database.sql')
DB_PATH   = os.path.join(BASE_DIR, '..', 'sql', 'spese.db')

def init_db():
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    with open(SQL_PATH, 'r', encoding='utf-8') as f:
        sql = f.read()

    # Esegui solo le istruzioni DDL e INSERT (non le SELECT di verifica)
    ddl_and_dml = []
    for stmt in sql.split(';'):
        s = stmt.strip()
        if s and not s.upper().startswith('SELECT'):
            ddl_and_dml.append(s)

    for stmt in ddl_and_dml:
        try:
            conn.execute(stmt)
        except sqlite3.Error as e:
            print(f"Avviso: {e} — istruzione ignorata.")

    conn.commit()
    conn.close()
    print(f"Database inizializzato: {os.path.abspath(DB_PATH)}")

if __name__ == '__main__':
    init_db()
