from database import get_connection


def buscar_todos_contatos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM contatos WHERE status = 'ativo' ORDER BY nome ASC"
    )
    contatos = cursor.fetchall()
    conn.close()
    return contatos


def buscar_contato_por_id(contato_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM contatos WHERE id = ?",
        (contato_id,)
    )
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


def atualizar_contato_banco(contato_id, nome, email, telefone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE contatos SET nome = ?, email = ?, telefone = ? WHERE id = ?",
        (nome, email, telefone, contato_id)
    )
    conn.commit()
    conn.close()


def email_ja_cadastrado(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM contatos WHERE email = ?",
        (email,)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


def email_pertence_a_outro(email, contato_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM contatos WHERE email = ? AND id != ?",
        (email, contato_id)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


def contato_possui_tarefas(contato_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) AS total FROM tarefas_contatos WHERE contato_id = ?",
        (contato_id,)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado["total"] > 0


def remover_contato_banco(contato_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tarefas_contatos WHERE contato_id = ?",
        (contato_id,)
    )
    cursor.execute(
        "UPDATE contatos SET status = 'bloqueado' WHERE id = ?",
        (contato_id,)
    )
    conn.commit()
    conn.close()


def buscar_tarefas_agrupadas_por_contato(status=None, contato_id=None):
    condicoes = ["c.status = 'ativo'"]
    parametros = []

    filtro_status = ""
    if status:
        filtro_status = "AND t.status = ?"
        parametros.append(status)

    if contato_id is not None:
        condicoes.append("c.id = ?")
        parametros.append(contato_id)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            c.id AS contato_id,
            c.nome AS responsavel,
            c.email AS email,
            c.telefone AS telefone,
            t.id AS tarefa_id,
            t.descricao AS descricao,
            t.status AS status,
            t.prazo AS prazo,
            t.prioridade AS prioridade
        FROM contatos c
        LEFT JOIN tarefas_contatos tc
            ON tc.contato_id = c.id
        LEFT JOIN tarefas t
            ON t.id = tc.tarefa_id {filtro_status}
        WHERE {" AND ".join(condicoes)}
        ORDER BY c.nome ASC, t.prazo ASC
    """, parametros)

    linhas = cursor.fetchall()
    conn.close()

    agrupados = {}

    for linha in linhas:
        grupo = agrupados.setdefault(linha["contato_id"], {
            "id": linha["contato_id"],
            "nome": linha["responsavel"],
            "email": linha["email"],
            "telefone": linha["telefone"],
            "tarefas": [],
        })

        if linha["tarefa_id"] is not None:
            grupo["tarefas"].append({
                "id": linha["tarefa_id"],
                "descricao": linha["descricao"],
                "status": linha["status"],
                "prazo": linha["prazo"],
                "prioridade": linha["prioridade"],
            })

    return list(agrupados.values())
