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
			id	 INTEGER PRIMARY KEY AUTOINCREMENT,
			nome	 TEXTO NOT NULL,
			email	 TEXT,
			telefone TEXT
		);

		CREATE TABLE IF NOT EXISTS tarefas (
			id		INTEGER PRIMARY KEY AUTOINCREMENT,
			descricao	TEXTO NOT NULL,
			prazo		TEXT,
			prioridade	TEXT NOT NULL DEFAULT 'media',
			status		TEXT NOT NULL DEFAULT 'fazer',
			FOREIGN KEY	(contato_id) REFERENCES contatos(id) ON DELETE SET NULL
		);
		
		CREATE TABLE IF NOT EXISTS tarefas_contatos (
			tarefa_id INTEGER NOT NULL,
			contato_id INTEGER NOT NULL,

			PRIMARY KEY (tarefa_id, contato_id),

			FOREIGN KEY (tarefa_id)
				REFERENCES tarefas(id)
				ON DELETE CASCADE,

			FOREIGN KEY (contato_id)
				REFERENCES contatos(id)
				ON DELETE CASCADE
		);
	""")
	conn.commit()
	conn.close()
