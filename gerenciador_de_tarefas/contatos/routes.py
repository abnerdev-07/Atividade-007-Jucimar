import config
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from contatos.models import (
    buscar_todos_contatos, inserir_contato_banco, email_ja_cadastrado,
    remover_contato_banco, buscar_contato_por_id,
    atualizar_contato_banco, email_pertence_a_outro,
    buscar_tarefas_agrupadas_por_contato
)
from database import get_connection

contatos_bp = Blueprint('contatos', __name__, url_prefix='/contatos')

@contatos_bp.route('/')
def listar_contatos():
    contatos = buscar_todos_contatos()
    return render_template('contatos/lista.html', contatos=contatos)

@contatos_bp.route('/novo', methods=['GET', 'POST'])
def novo_contato():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()

        if not nome or not email:
            flash('Erro: Os campos Nome e E-mail são obrigatórios!', 'danger')
            return redirect(url_for('contatos.novo_contato'))

        if email_ja_cadastrado(email):
            flash('Erro: Este e-mail já está sendo utilizado por outro membro do time!', 'danger')
            return redirect(url_for('contatos.novo_contato'))

        inserir_contato_banco(nome, email, telefone)
        flash('Colaborador cadastrado com sucesso!', 'success')
        return redirect(url_for('contatos.listar_contatos'))

    return render_template('contatos/formulario.html')

@contatos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_contato(id):
    contato = buscar_contato_por_id(id)
    if contato is None:
        abort(404)

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()

        if not nome or not email:
            flash('Erro: Os campos Nome e E-mail são obrigatórios!', 'danger')
            return redirect(url_for('contatos.editar_contato', id=id))

        if email_pertence_a_outro(email, id):
            flash('Erro: Este e-mail já está sendo utilizado por outro membro do time!', 'danger')
            return redirect(url_for('contatos.editar_contato', id=id))

        atualizar_contato_banco(id, nome, email, telefone)
        flash('Colaborador atualizado com sucesso!', 'success')
        return redirect(url_for('contatos.listar_contatos'))

    return render_template('contatos/formulario.html', contato=contato)

@contatos_bp.route('/apagar/<int:id>', methods=['POST'])
def apagar_contato(id):
    remover_contato_banco(id)
    flash('Colaborador bloqueado com sucesso! Suas tarefas foram liberadas para reatribuição.', 'success')
    return redirect(url_for('contatos.listar_contatos'))

@contatos_bp.route('/agrupados-por-responsavel')
def dados_agrupados():
    status = request.args.get('status') or None
    contato_id = request.args.get('contato', type=int)

    if status and status not in config.STATUS_OPCOES:
        status = None

    grupos = buscar_tarefas_agrupadas_por_contato(status=status, contato_id=contato_id)
    return render_template(
        'tarefas/quadro_admin.html',
        grupos=grupos,
        contatos=buscar_todos_contatos(),
        status_opcoes=config.STATUS_OPCOES,
        status_atual=status,
        contato_atual=contato_id,
    )

@contatos_bp.route('/filtrar-por-contato/<int:contato_id>')
def filtrar_por_contato(contato_id):
    contato = buscar_contato_por_id(contato_id)
    if not contato:
        flash('Colaborador não localizado para aplicação do filtro.', 'danger')
        return redirect(url_for('contatos.listar_contatos'))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarefas WHERE contato_id = ?", (contato_id,))
    tarefas_filtradas = cursor.fetchall()
    conn.close()
    return render_template('tarefas/quadro.html', contato=contato, tarefas=tarefas_filtradas)