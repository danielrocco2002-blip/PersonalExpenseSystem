import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'sql', 'spese.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ─────────────────────────────────────────────
# MODULO 1 — Gestione Categorie
# ─────────────────────────────────────────────
def gestione_categorie():
    print("\n--- GESTIONE CATEGORIE ---")
    nome = input("Inserisci il nome della categoria: ").strip()
    if not nome:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM categorie WHERE nome = ?", (nome,))
    if cur.fetchone():
        print("Errore: La categoria esiste già.")
    else:
        cur.execute("INSERT INTO categorie (nome) VALUES (?)", (nome,))
        conn.commit()
        print("Categoria inserita correttamente.")
    conn.close()

# ─────────────────────────────────────────────
# MODULO 2 — Inserimento Spesa
# ─────────────────────────────────────────────
def inserisci_spesa():
    print("\n--- INSERISCI SPESA ---")
    data = input("Data (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        print("Errore: formato data non valido. Usa YYYY-MM-DD.")
        return

    try:
        importo = float(input("Importo: ").strip())
    except ValueError:
        print("Errore: importo non valido.")
        return

    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return

    categoria = input("Nome categoria: ").strip()
    descrizione = input("Descrizione (facoltativa): ").strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM categorie WHERE nome = ?", (categoria,))
    row = cur.fetchone()
    if not row:
        print("Errore: la categoria non esiste.")
        conn.close()
        return

    cat_id = row[0]
    cur.execute(
        "INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES (?, ?, ?, ?)",
        (data, importo, cat_id, descrizione if descrizione else None)
    )
    conn.commit()
    print("Spesa inserita correttamente.")
    conn.close()

# ─────────────────────────────────────────────
# MODULO 3 — Definizione Budget Mensile
# ─────────────────────────────────────────────
def definisci_budget():
    print("\n--- DEFINISCI BUDGET MENSILE ---")
    mese = input("Mese (YYYY-MM): ").strip()
    try:
        datetime.strptime(mese, "%Y-%m")
    except ValueError:
        print("Errore: formato mese non valido. Usa YYYY-MM.")
        return

    categoria = input("Nome categoria: ").strip()
    try:
        importo = float(input("Importo budget: ").strip())
    except ValueError:
        print("Errore: importo non valido.")
        return

    if importo <= 0:
        print("Errore: il budget deve essere maggiore di zero.")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM categorie WHERE nome = ?", (categoria,))
    row = cur.fetchone()
    if not row:
        print("Errore: la categoria non esiste.")
        conn.close()
        return

    cat_id = row[0]
    cur.execute(
        "SELECT id FROM budget WHERE mese = ? AND categoria_id = ?", (mese, cat_id)
    )
    existing = cur.fetchone()
    if existing:
        cur.execute(
            "UPDATE budget SET importo = ? WHERE mese = ? AND categoria_id = ?",
            (importo, mese, cat_id)
        )
    else:
        cur.execute(
            "INSERT INTO budget (mese, categoria_id, importo) VALUES (?, ?, ?)",
            (mese, cat_id, importo)
        )
    conn.commit()
    print("Budget mensile salvato correttamente.")
    conn.close()

# ─────────────────────────────────────────────
# MODULO 4 — Report
# ─────────────────────────────────────────────
def report_totale_per_categoria():
    print("\n--- TOTALE SPESE PER CATEGORIA ---")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.nome, COALESCE(SUM(s.importo), 0) AS totale
        FROM categorie c
        LEFT JOIN spese s ON s.categoria_id = c.id
        GROUP BY c.id
        ORDER BY totale DESC
    """)
    rows = cur.fetchall()
    conn.close()

    print(f"\n{'Categoria':<20} {'Totale Speso':>15}")
    print("-" * 37)
    for nome, totale in rows:
        print(f"{nome:<20} {totale:>15.2f}")

def report_spese_vs_budget():
    print("\n--- SPESE MENSILI VS BUDGET ---")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.mese, c.nome,
               b.importo AS budget,
               COALESCE(SUM(s.importo), 0) AS speso
        FROM budget b
        JOIN categorie c ON c.id = b.categoria_id
        LEFT JOIN spese s ON s.categoria_id = b.categoria_id
                          AND strftime('%Y-%m', s.data) = b.mese
        GROUP BY b.mese, b.categoria_id
        ORDER BY b.mese, c.nome
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("Nessun budget definito.")
        return

    for mese, cat, budget, speso in rows:
        stato = "SUPERAMENTO BUDGET" if speso > budget else "OK"
        print(f"\nMese: {mese}")
        print(f"Categoria: {cat}")
        print(f"Budget: {budget:.2f}")
        print(f"Speso: {speso:.2f}")
        print(f"Stato: {stato}")

def report_elenco_spese():
    print("\n--- ELENCO COMPLETO SPESE ---")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.data, c.nome, s.importo, COALESCE(s.descrizione, '')
        FROM spese s
        JOIN categorie c ON c.id = s.categoria_id
        ORDER BY s.data
    """)
    rows = cur.fetchall()
    conn.close()

    print(f"\n{'Data':<12} {'Categoria':<20} {'Importo':>10} {'Descrizione'}")
    print("-" * 65)
    for data, cat, importo, desc in rows:
        print(f"{data:<12} {cat:<20} {importo:>10.2f} {desc}")

def visualizza_report():
    while True:
        print("""
--- MENU REPORT ---
1. Totale spese per categoria
2. Spese mensili vs budget
3. Elenco completo delle spese ordinate per data
4. Ritorna al menu principale
""")
        scelta = input("Inserisci la tua scelta: ").strip()
        if scelta == '1':
            report_totale_per_categoria()
        elif scelta == '2':
            report_spese_vs_budget()
        elif scelta == '3':
            report_elenco_spese()
        elif scelta == '4':
            break
        else:
            print("Scelta non valida. Riprovare.")

# ─────────────────────────────────────────────
# MENU PRINCIPALE
# ─────────────────────────────────────────────
def main():
    # Assicura che la directory del DB esista
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)

    print("=" * 40)
    print("  BENVENUTO NEL SISTEMA SPESE PERSONALI")
    print("=" * 40)

    while True:
        print("""
-------------------------
 SISTEMA SPESE PERSONALI
-------------------------
1. Gestione Categorie
2. Inserisci Spesa
3. Definisci Budget Mensile
4. Visualizza Report
5. Esci
-------------------------""")
        scelta = input("Inserisci la tua scelta: ").strip()

        if scelta == '1':
            gestione_categorie()
        elif scelta == '2':
            inserisci_spesa()
        elif scelta == '3':
            definisci_budget()
        elif scelta == '4':
            visualizza_report()
        elif scelta == '5':
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprovare.")

if __name__ == '__main__':
    main()
