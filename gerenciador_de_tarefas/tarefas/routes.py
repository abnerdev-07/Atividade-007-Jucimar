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
    atualizar_tarefa
)

from database import get_connection
import config


tarefas_bp = Blueprint("tarefas", __name__)


@tarefas_bp.route("/tarefas", methods=["GET"])
def listar():
    tarefas = listar_tarefas()
    return render_template("tarefas/lista.html", tarefas=tarefas)


@tarefas_bp.route("/tarefas/nova", methods=["GET", "POST"])
def nova_tarefa():
    conn = get_connection()

    try:
        contatos = conn.execute(
            "SELECT id, nome FROM contatos ORDER BY nome"
        ).fetchall()

        contatos = [dict(contato) for contato in contatos]
    finally:
        conn.close()

    if request.method == "POST":
        descricao = request.form.get("descricao", "").strip()
        prazo = request.form.get("prazo") or None
        prioridade = request.form.get("prioridade", "media")
        status = request.form.get("status", "fazer")
        contatos_ids = request.form.getlist("contatos_ids", type=int)

        if not descricao or not contatos_ids:
            flash(
                "A descrição e pelo menos um responsável são obrigatórios.",
                "danger"
            )
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
        "tarefas/adicionar_tarefa.html",
        contatos=contatos,
        prioridades=config.PRIORIDADES,
        status_opcoes=config.STATUS_OPCOES
    )


@tarefas_bp.route(
    "/tarefas/<int:tarefa_id>/editar",
    methods=["GET", "POST"]
)
def editar_tarefa(tarefa_id):
    tarefa = buscar_tarefa(tarefa_id)

    if tarefa is None:
        abort(404)

    conn = get_connection()

    try:
        contatos = conn.execute(
            "SELECT id, nome FROM contatos ORDER BY nome"
        ).fetchall()

        contatos = [dict(contato) for contato in contatos]
    finally:
        conn.close()

    tarefa_contat_ids = [
        contato["id"] for contato in tarefa["contatos"]
    ]

    if request.method == "POST":
        descricao = request.form.get("descricao", "").strip()
        prazo = request.form.get("prazo") or None
        prioridade = request.form.get("prioridade", "media")
        status = request.form.get("status", "fazer")
        contatos_ids = request.form.getlist("contatos_ids", type=int)

        if not descricao or not contatos_ids:
            flash(
                "A descrição e pelo menos um responsável são obrigatórios.",
                "danger"
            )
            return redirect(
                url_for("tarefas.editar_tarefa", tarefa_id=tarefa_id)
            )

        if prioridade not in config.PRIORIDADES:
            flash("Prioridade inválida.", "danger")
            return redirect(
                url_for("tarefas.editar_tarefa", tarefa_id=tarefa_id)
            )

        if status not in config.STATUS_OPCOES:
            flash("Status inválido.", "danger")
            return redirect(
                url_for("tarefas.editar_tarefa", tarefa_id=tarefa_id)
            )

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
        "tarefas/editar_tarefa.html",
        tarefa=tarefa,
        contatos=contatos,
        tarefa_contat_ids=tarefa_contat_ids,
        prioridades=config.PRIORIDADES,
        status_opcoes=config.STATUS_OPCOES
    )
