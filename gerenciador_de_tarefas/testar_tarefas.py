import os
import sqlite3
import tempfile

import config
config.DATABASE = os.path.join(tempfile.mkdtemp(), "teste.db")   # banco temporario, nao mexe no seu

from database import init_db, get_connection
from tarefas.models import (
    criar_tarefa, listar_tarefas, buscar_tarefa, atualizar_tarefa, excluir_tarefa,
)

falhas = 0


def conferir(nome, condicao):
    global falhas
    print(("OK   " if condicao else "ERRO ") + nome)
    if not condicao:
        falhas += 1


init_db()

# prepara 2 contatos
conn = get_connection()
conn.execute("INSERT INTO contatos (nome) VALUES ('Ana'), ('Bruno')")
conn.commit()
conn.close()

# 1. criar (com 2 responsaveis)
tid = criar_tarefa("Estudar Flask", "2026-10-20", "alta", "fazer", [1, 2])
conferir("criar_tarefa devolve um id", isinstance(tid, int))

# 2. listar
lista = listar_tarefas()
conferir("listar_tarefas traz 1 tarefa", len(lista) == 1)
conferir("a tarefa tem 2 responsaveis", len(lista[0]["contatos"]) == 2)

# 3. buscar
t = buscar_tarefa(tid)
conferir("buscar_tarefa acha a tarefa", t is not None and t["descricao"] == "Estudar Flask")
conferir("buscar_tarefa traz os responsaveis", [c["nome"] for c in t["contatos"]] == ["Ana", "Bruno"])
conferir("buscar_tarefa de id inexistente devolve None", buscar_tarefa(999) is None)

# 4. atualizar (muda status e deixa so 1 responsavel)
ok = atualizar_tarefa(tid, "Estudar Flask hoje", "2026-10-21", "media", "fazendo", [2])
t = buscar_tarefa(tid)
conferir("atualizar_tarefa devolve True", ok is True)
conferir("atualizar mudou descricao e status", t["descricao"] == "Estudar Flask hoje" and t["status"] == "fazendo")
conferir("atualizar trocou os responsaveis", [c["nome"] for c in t["contatos"]] == ["Bruno"])
conferir("atualizar tarefa inexistente devolve False", atualizar_tarefa(999, "x") is False)

# 5. regra: contato com tarefa nao pode ser apagado
conn = get_connection()
try:
    conn.execute("DELETE FROM contatos WHERE id = 2")
    conn.commit()
    bloqueou = False
except sqlite3.IntegrityError:
    bloqueou = True
conn.close()
conferir("apagar contato que tem tarefa e bloqueado", bloqueou)

# 6. excluir
conferir("excluir_tarefa devolve True", excluir_tarefa(tid) is True)
conferir("tarefa some depois de excluida", buscar_tarefa(tid) is None)
conferir("excluir tarefa inexistente devolve False", excluir_tarefa(tid) is False)

print()
print("TUDO CERTO" if falhas == 0 else f"{falhas} teste(s) com ERRO")