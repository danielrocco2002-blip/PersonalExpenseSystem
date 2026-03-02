-- ============================================================
-- SISTEMA DI GESTIONE DELLE SPESE PERSONALI E DEL BUDGET
-- Script SQL — Creazione database, vincoli e dati di esempio
-- ============================================================

-- ─────────────────────────────────────────────
-- 1. CREAZIONE TABELLE
-- ─────────────────────────────────────────────

-- Tabella CATEGORIE
CREATE TABLE IF NOT EXISTS categorie (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT    NOT NULL UNIQUE            -- UNIQUE + NOT NULL
);

-- Tabella SPESE
CREATE TABLE IF NOT EXISTS spese (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    data         TEXT    NOT NULL,
    importo      REAL    NOT NULL CHECK (importo > 0),   -- CHECK
    categoria_id INTEGER NOT NULL,
    descrizione  TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorie(id) -- FOREIGN KEY
);

-- Tabella BUDGET
CREATE TABLE IF NOT EXISTS budget (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    mese         TEXT    NOT NULL,                       -- formato YYYY-MM
    categoria_id INTEGER NOT NULL,
    importo      REAL    NOT NULL CHECK (importo > 0),   -- CHECK
    UNIQUE (mese, categoria_id),                         -- UNIQUE su coppia
    FOREIGN KEY (categoria_id) REFERENCES categorie(id) -- FOREIGN KEY
);

-- ─────────────────────────────────────────────
-- 2. DATI DI ESEMPIO
-- ─────────────────────────────────────────────

-- Categorie
INSERT OR IGNORE INTO categorie (nome) VALUES ('Alimentari');
INSERT OR IGNORE INTO categorie (nome) VALUES ('Trasporti');
INSERT OR IGNORE INTO categorie (nome) VALUES ('Svago');
INSERT OR IGNORE INTO categorie (nome) VALUES ('Salute');
INSERT OR IGNORE INTO categorie (nome) VALUES ('Utenze');

-- Spese
INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES
    ('2025-01-05',  85.50, 1, 'Spesa settimanale'),
    ('2025-01-10',  30.00, 2, 'Abbonamento bus'),
    ('2025-01-12', 120.00, 1, 'Spesa mensile grande'),
    ('2025-01-15',  25.00, 3, 'Cinema'),
    ('2025-01-18',  45.00, 4, 'Farmacia'),
    ('2025-01-20',  90.00, 1, 'Supermercato'),
    ('2025-01-22',  50.00, 5, 'Bolletta luce'),
    ('2025-01-25',  20.00, 2, 'Benzina'),
    ('2025-02-03',  70.00, 1, 'Spesa settimanale'),
    ('2025-02-08',  40.00, 3, 'Ristorante'),
    ('2025-02-14',  60.00, 2, 'Treno'),
    ('2025-02-20',  35.00, 4, 'Visita medica');

-- Budget mensili
INSERT OR IGNORE INTO budget (mese, categoria_id, importo) VALUES
    ('2025-01', 1, 300.00),   -- Alimentari gennaio: budget 300
    ('2025-01', 2,  80.00),   -- Trasporti gennaio: budget 80
    ('2025-01', 3,  50.00),   -- Svago gennaio: budget 50
    ('2025-02', 1, 250.00),   -- Alimentari febbraio: budget 250
    ('2025-02', 2, 100.00),   -- Trasporti febbraio: budget 100
    ('2025-02', 3,  80.00);   -- Svago febbraio: budget 80

-- ─────────────────────────────────────────────
-- 3. QUERY DI VERIFICA / REPORT
-- ─────────────────────────────────────────────

-- Report 1: Totale spese per categoria
SELECT c.nome AS Categoria, COALESCE(SUM(s.importo), 0) AS TotaleSpeso
FROM categorie c
LEFT JOIN spese s ON s.categoria_id = c.id
GROUP BY c.id
ORDER BY TotaleSpeso DESC;

-- Report 2: Spese mensili vs budget
SELECT b.mese, c.nome AS Categoria,
       b.importo AS Budget,
       COALESCE(SUM(s.importo), 0) AS Speso,
       CASE WHEN COALESCE(SUM(s.importo), 0) > b.importo
            THEN 'SUPERAMENTO BUDGET'
            ELSE 'OK'
       END AS Stato
FROM budget b
JOIN categorie c ON c.id = b.categoria_id
LEFT JOIN spese s ON s.categoria_id = b.categoria_id
                  AND strftime('%Y-%m', s.data) = b.mese
GROUP BY b.mese, b.categoria_id
ORDER BY b.mese, c.nome;

-- Report 3: Elenco completo spese ordinate per data
SELECT s.data, c.nome AS Categoria, s.importo, COALESCE(s.descrizione, '') AS Descrizione
FROM spese s
JOIN categorie c ON c.id = s.categoria_id
ORDER BY s.data;
