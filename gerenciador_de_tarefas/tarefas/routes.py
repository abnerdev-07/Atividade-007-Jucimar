from flask import Blueprint, render_template, request, redirect, url_for, abort
from tarefas.models import (
    criar_tarefa,
    listar_tarefas,
    buscar_tarefa,
    atualizar_tarefa
)
from database import get_connection
import config

tarefas_bp = Blueprint("tarefas", __name__)


@tarefas_bp.route("/tarefas", methods=["GET"])
def listar():
    tarefas = listar_tarefas()

    return render_template(
        "tarefas/lista.html",
        tarefas=tarefas
    )

@tarefas_bp.route("/tarefas/nova", methods=["GET", "POST"])
def nova_tarefa():
    conn = get_connection()

    try:
        contatos = conn.execute(
            "SELECT id, nome FROM contatos ORDER BY nome"
        ).fetchall()
    finally:
        conn.close()

    if request.method == "POST":
        descricao = request.form.get("descricao", "").strip()
        prazo = request.form.get("prazo") or None
        prioridade = request.form.get("prioridade", "media")
        status = request.form.get("status", "fazer")
        contatos_ids = request.form.getlist("contatos_ids", type=int)

        if not descricao:
            return "A descrição é obrigatória.", 400

        if prioridade not in config.PRIORIDADES:
            return "Prioridade inválida.", 400

        if status not in config.STATUS_OPCOES:
            return "Status inválido.", 400

        criar_tarefa(
            descricao=descricao,
            prazo=prazo,
            prioridade=prioridade,
            status=status,
            contatos_ids=contatos_ids
        )

        return redirect(url_for("tarefas.listar"))

    return render_template(
        "tarefas/formulario.html",
        tarefa=None,
        contatos=contatos,
        prioridades=config.PRIORIDADES,
        status_opcoes=config.STATUS_OPCOES
    )


@tarefas_bp.route("/tarefas/<int:tarefa_id>/editar", methods=["GET", "POST"])
def editar_tarefa(tarefa_id):
    tarefa = buscar_tarefa(tarefa_id)

    if tarefa is None:
        abort(404)

    conn = get_connection()
    try:
        contatos = conn.execute(
            "SELECT id, nome FROM contatos ORDER BY nome"
        ).fetchall()
    finally:
        conn.close()

    if request.method == "POST":
        descricao = request.form.get("descricao", "").strip()
        prazo = request.form.get("prazo") or None
        prioridade = request.form.get("prioridade", "media")
        status = request.form.get("status", "fazer")
        contatos_ids = request.form.getlist("contatos_ids", type=int)

        if not descricao:
            return "A descrição é obrigatória.", 400

        if prioridade not in config.PRIORIDADES:
            return "Prioridade inválida.", 400

        if status not in config.STATUS_OPCOES:
            return "Status inválido.", 400

        atualizar_tarefa(
            tarefa_id=tarefa_id,
            descricao=descricao,
            prazo=prazo,
            prioridade=prioridade,
            status=status,
            contatos_ids=contatos_ids
        )

        return redirect(url_for("tarefas.listar"))

    return render_template(
        "tarefas/formulario.html",
        tarefa=tarefa,
        contatos=contatos,
        prioridades=config.PRIORIDADES,
        status_opcoes=config.STATUS_OPCOES
    )
