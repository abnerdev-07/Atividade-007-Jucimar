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
            status      TEXT NOT NULL DEFAULT 'fazer'
        );

        CREATE TABLE IF NOT EXISTS tarefas_contatos (
            tarefa_id  INTEGER NOT NULL,
            contato_id INTEGER NOT NULL,
            PRIMARY KEY (tarefa_id, contato_id),
            FOREIGN KEY (tarefa_id)  REFERENCES tarefas(id)  ON DELETE CASCADE,
            FOREIGN KEY (contato_id) REFERENCES contatos(id) ON DELETE RESTRICT
        );
    """)
    conn.commit()
    conn.close()