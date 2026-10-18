from database import get_connection


def buscar_todos_contatos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contatos WHERE status = 'ativo' ORDER BY nome ASC")
    contatos = cursor.fetchall()
    conn.close()
    return contatos


def buscar_contato_por_id(contato_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contatos WHERE id = ?", (contato_id,))
    contato = cursor.fetchone()
    conn.close()
    return contato


def inserir_contato_banco(nome, email, telefone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contatos (nome, email, telefone) VALUES (?, ?, ?)",
        (nome, email, telefone)
    )
    conn.commit()
    conn.close()


def email_ja_cadastrado(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM contatos WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


def contato_possui_tarefas(contato_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) AS total FROM tarefas WHERE contato_id = ?",
        (contato_id,)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado["total"] > 0


def remover_contato_banco(contato_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET contato_id = NULL WHERE contato_id = ?", (contato_id,))
    cursor.execute("UPDATE contatos SET status = 'bloqueado' WHERE id = ?", (contato_id,))
    conn.commit()
    conn.close()
