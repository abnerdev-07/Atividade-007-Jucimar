import sqlite3
import config

def get_connection():
    conn = sqlite3.connect(config.DATABASE)
    conn.row_factory = sqlite3.Row
    
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS contatos (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nome     TEXT NOT NULL,
            email    TEXT,
            telefone TEXT
        );

        CREATE TABLE IF NOT EXISTS tarefas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao   TEXT NOT NULL,
            prazo       TEXT,
            prioridade  TEXT NOT NULL DEFAULT 'media',
            status      TEXT NOT NULL DEFAULT 'fazer',
            contato_id  INTEGER,
            FOREIGN KEY (contato_id) REFERENCES contatos(id)
        );
    """)
    conn.commit()
    conn.close()
