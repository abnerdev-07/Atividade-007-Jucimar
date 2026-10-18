#contatos/models
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


def email_ja_cadastrado(email, ignorar_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if ignorar_id is None:
        cursor.execute("SELECT id FROM contatos WHERE email = ?", (email,))
    else:
        cursor.execute(
            "SELECT id FROM contatos WHERE email = ? AND id != ?",
            (email, ignorar_id)
        )
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


def atualizar_contato_banco(contato_id, nome, email, telefone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE contatos SET nome = ?, email = ?, telefone = ? WHERE id = ?",
        (nome, email, telefone, contato_id)
    )
    conn.commit()
    atualizado = cursor.rowcount > 0
    conn.close()
    return atualizado


def contato_possui_tarefas(contato_id):
    """True se o contato ainda e responsavel por alguma tarefa NAO concluida."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM tarefas_contatos tc
        JOIN tarefas t ON t.id = tc.tarefa_id
        WHERE tc.contato_id = ? AND t.status != 'concluida'
        """,
        (contato_id,)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado["total"] > 0


def remover_contato_banco(contato_id):
    """Bloqueia o contato (nao apaga). A checagem de tarefas e feita na rota."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE contatos SET status = 'bloqueado' WHERE id = ?", (contato_id,))
    conn.commit()
    conn.close()