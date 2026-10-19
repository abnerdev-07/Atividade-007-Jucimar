from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    flash
)

from tarefas.models import (
    criar_tarefa,
    listar_tarefas,
    buscar_tarefa,
    atualizar_tarefa,
    excluir_tarefa,
    status_efetivo
)

from contatos.models import buscar_todos_contatos
import config


tarefas_bp = Blueprint("tarefas", __name__)


@tarefas_bp.route("/tarefas", methods=["GET"])
def listar():
    tarefas = listar_tarefas()

    # Filtro por contato: /tarefas?contato=3 mostra so as tarefas do contato 3
    contato_id = request.args.get("contato", type=int)
    if contato_id:
        tarefas = [
            t for t in tarefas
            if any(c["id"] == contato_id for c in t["contatos"])
        ]

    for t in tarefas:
        t["status_final"] = status_efetivo(t)

    return render_template(
        "tarefas/lista.html",
        tarefas=tarefas,
        contatos=buscar_todos_contatos(),
        contato_filtrado=contato_id
    )


@tarefas_bp.route("/tarefas/nova", methods=["GET", "POST"])
def nova_tarefa():
    contatos = [dict(c) for c in buscar_todos_contatos()]

    if request.method == "POST":
        descricao = request.form.get("descricao", "").strip()
        prazo = request.form.get("prazo") or None
        prioridade = request.form.get("prioridade", "media")
        status = request.form.get("status", "fazer")
        contatos_ids = request.form.getlist("contatos_ids", type=int)

        if not descricao or not contatos_ids:
            flash("A descrição e pelo menos um responsável são obrigatórios.", "danger")
            return redirect(url_for("tarefas.nova_tarefa"))

        if prioridade not in config.PRIORIDADES:
            flash("Prioridade inválida.", "danger")
            return redirect(url_for("tarefas.nova_tarefa"))

        if status not in config.STATUS_OPCOES:
            flash("Status inválido.", "danger")
            return redirect(url_for("tarefas.nova_tarefa"))

        criar_tarefa(
            descricao=descricao,
            prazo=prazo,
            prioridade=prioridade,
            status=status,
            contatos_ids=contatos_ids
        )

        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for("tarefas.listar"))

    return render_template(
        "contatos/formulario.html",
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

    contatos = [dict(c) for c in buscar_todos_contatos()]

    if request.method == "POST":
        descricao = request.form.get("descricao", "").strip()
        prazo = request.form.get("prazo") or None
        prioridade = request.form.get("prioridade", "media")
        status = request.form.get("status", "fazer")
        contatos_ids = request.form.getlist("contatos_ids", type=int)

        if not descricao or not contatos_ids:
            flash("A descrição e pelo menos um responsável são obrigatórios.", "danger")
            return redirect(url_for("tarefas.editar_tarefa", tarefa_id=tarefa_id))

        if prioridade not in config.PRIORIDADES:
            flash("Prioridade inválida.", "danger")
            return redirect(url_for("tarefas.editar_tarefa", tarefa_id=tarefa_id))

        if status not in config.STATUS_OPCOES:
            flash("Status inválido.", "danger")
            return redirect(url_for("tarefas.editar_tarefa", tarefa_id=tarefa_id))

        atualizar_tarefa(
            tarefa_id=tarefa_id,
            descricao=descricao,
            prazo=prazo,
            prioridade=prioridade,
            status=status,
            contatos_ids=contatos_ids
        )

        flash("Tarefa atualizada com sucesso!", "success")
        return redirect(url_for("tarefas.listar"))

    return render_template(
        "tarefas/formulario.html",
        tarefa=tarefa,
        contatos=contatos,
        prioridades=config.PRIORIDADES,
        status_opcoes=config.STATUS_OPCOES
    )


@tarefas_bp.route("/tarefas/<int:tarefa_id>/excluir", methods=["POST"])
def remover_tarefa(tarefa_id):
    excluida = excluir_tarefa(tarefa_id)

    if not excluida:
        abort(404)

    return redirect(url_for("tarefas.listar"))
