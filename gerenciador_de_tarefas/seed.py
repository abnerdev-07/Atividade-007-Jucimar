from datetime import date, timedelta

from database import get_connection, init_db

CONTATOS = [
    ("Matheus", "matheus@email.com", "92 99999-0001"),
    ("Abner", "abner@email.com", "92 99999-0002"),
    ("Aline", "aline@email.com", "92 99999-0003"),
    ("Anthony", "anthony@email.com", "92 99999-0004"),
]

hoje = date.today()

# (descricao, prazo, prioridade, status, indices dos contatos responsaveis)
TAREFAS = [
    ("Criar tela de login", hoje + timedelta(days=5), "alta", "fazer", [0]),
    ("Escrever o README", hoje + timedelta(days=7), "media", "fazendo", [1]),
    ("Configurar o banco de dados", hoje - timedelta(days=2), "alta", "concluida", [2]),
    ("Revisar os pull requests", hoje - timedelta(days=3), "media", "atrasada", [3]),
    ("Montar o cronograma", hoje + timedelta(days=10), "baixa", "fazer", [0, 1]),
    ("Testar o formulário de tarefas", hoje + timedelta(days=2), "alta", "fazendo", [2]),
    ("Corrigir bugs da lista", hoje - timedelta(days=1), "baixa", "atrasada", [1, 3]),
]


def popular():
    init_db()
    conn = get_connection()

    # Limpa antes, para rodar o script várias vezes sem duplicar dados
    conn.execute("DELETE FROM tarefas_contatos")
    conn.execute("DELETE FROM tarefas")
    conn.execute("DELETE FROM contatos")

    ids = []
    for nome, email, telefone in CONTATOS:
        cursor = conn.execute(
            "INSERT INTO contatos (nome, email, telefone) VALUES (?, ?, ?)",
            (nome, email, telefone),
        )
        ids.append(cursor.lastrowid)

    for descricao, prazo, prioridade, status, indices in TAREFAS:
        cursor = conn.execute(
            "INSERT INTO tarefas (descricao, prazo, prioridade, status) "
            "VALUES (?, ?, ?, ?)",
            (descricao, prazo.isoformat(), prioridade, status),
        )
        tarefa_id = cursor.lastrowid
        for indice in indices:
            conn.execute(
                "INSERT INTO tarefas_contatos (tarefa_id, contato_id) VALUES (?, ?)",
                (tarefa_id, ids[indice]),
            )

    conn.commit()
    conn.close()
    print(f"{len(CONTATOS)} contatos e {len(TAREFAS)} tarefas cadastrados.")


if __name__ == "__main__":
    popular()
