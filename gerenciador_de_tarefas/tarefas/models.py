from datetime import date

from database import get_connection


def status_efetivo(tarefa):
    """Devolve 'atrasada' se o prazo já passou e a tarefa não está concluída.
    Caso contrário, devolve o status que está salvo."""
    status = tarefa["status"]
    prazo = tarefa["prazo"]

    if status == "concluida" or not prazo:
        return status

    try:
        vencimento = date.fromisoformat(prazo)   # prazo no formato 2026-10-17
    except ValueError:
        return status

    if vencimento < date.today():
        return "atrasada"
    return status


def criar_tarefa(
    descricao,
    prazo=None,
    prioridade="media",
    status="fazer",
    contatos_ids=None
):
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO tarefas
                (descricao, prazo, prioridade, status)
            VALUES (?, ?, ?, ?)
            """,
            (descricao, prazo, prioridade, status)
        )

        tarefa_id = cursor.lastrowid

        if contatos_ids:
            for contato_id in set(contatos_ids):
                conn.execute(
                    """
                    INSERT INTO tarefas_contatos
                        (tarefa_id, contato_id)
                    VALUES (?, ?)
                    """,
                    (tarefa_id, contato_id)
                )

        conn.commit()
        return tarefa_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def listar_tarefas():
    conn = get_connection()

    try:
        tarefas = conn.execute("""
            SELECT id, descricao, prazo,
                   prioridade, status
            FROM tarefas
            ORDER BY id DESC
        """).fetchall()

        resultado = []

        for tarefa in tarefas:
            contatos = conn.execute("""
                SELECT c.id, c.nome
                FROM contatos c
                JOIN tarefas_contatos tc
                    ON c.id = tc.contato_id
                WHERE tc.tarefa_id = ?
                ORDER BY c.nome
            """, (tarefa["id"],)).fetchall()

            dados = dict(tarefa)
            dados["contatos"] = [
                dict(contato) for contato in contatos
            ]

            resultado.append(dados)

        return resultado

    finally:
        conn.close()


def buscar_tarefa(tarefa_id):
    conn = get_connection()

    try:
        tarefa = conn.execute(
            "SELECT id, descricao, prazo, prioridade, status FROM tarefas WHERE id = ?",
            (tarefa_id,)
        ).fetchone()

        if tarefa is None:
            return None

        contatos = conn.execute("""
            SELECT c.id, c.nome
            FROM contatos c
            JOIN tarefas_contatos tc ON c.id = tc.contato_id
            WHERE tc.tarefa_id = ?
            ORDER BY c.nome
        """, (tarefa_id,)).fetchall()

        dados = dict(tarefa)
        dados["contatos"] = [dict(c) for c in contatos]
        return dados

    finally:
        conn.close()


def atualizar_tarefa(
    tarefa_id,
    descricao,
    prazo=None,
    prioridade="media",
    status="fazer",
    contatos_ids=None
):
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            UPDATE tarefas
            SET descricao = ?,
                prazo = ?,
                prioridade = ?,
                status = ?
            WHERE id = ?
            """,
            (descricao, prazo, prioridade, status, tarefa_id)
        )

        if cursor.rowcount == 0:
            return False

        if contatos_ids is not None:
            conn.execute(
                "DELETE FROM tarefas_contatos WHERE tarefa_id = ?",
                (tarefa_id,)
            )

            for contato_id in set(contatos_ids):
                conn.execute(
                    """
                    INSERT INTO tarefas_contatos
                    (tarefa_id, contato_id)
                    VALUES (?, ?)
                    """,
                    (tarefa_id, contato_id)
                )

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def excluir_tarefa(tarefa_id):
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            DELETE FROM tarefas
            WHERE id = ?
            """,
            (tarefa_id,)
        )

        conn.commit()

        return cursor.rowcount > 0

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()