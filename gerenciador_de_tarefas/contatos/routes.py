#contatos/routes
from flask import Blueprint, render_template, request, redirect, url_for, flash
from contatos.models import (
    buscar_todos_contatos, inserir_contato_banco, email_ja_cadastrado,
    remover_contato_banco, buscar_contato_por_id, atualizar_contato_banco,
    contato_possui_tarefas
)
from tarefas.models import status_efetivo
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
        flash('Colaborador não localizado.', 'danger')
        return redirect(url_for('contatos.listar_contatos'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()

        if not nome or not email:
            flash('Erro: Os campos Nome e E-mail são obrigatórios!', 'danger')
            return redirect(url_for('contatos.editar_contato', id=id))

        if email_ja_cadastrado(email, ignorar_id=id):
            flash('Erro: Este e-mail já está sendo utilizado por outro membro do time!', 'danger')
            return redirect(url_for('contatos.editar_contato', id=id))

        atualizar_contato_banco(id, nome, email, telefone)
        flash('Colaborador atualizado com sucesso!', 'success')
        return redirect(url_for('contatos.listar_contatos'))

    return render_template('contatos/formulario.html', contato=contato)

@contatos_bp.route('/apagar/<int:id>', methods=['POST'])
def apagar_contato(id):
    # Regra do grupo: nao bloqueia quem ainda e responsavel por tarefa nao concluida.
    # O admin precisa reatribuir as tarefas antes (editando cada tarefa).
    if contato_possui_tarefas(id):
        flash('Este colaborador ainda é responsável por tarefas. Reatribua as tarefas antes de bloqueá-lo.', 'danger')
        return redirect(url_for('contatos.listar_contatos'))

    remover_contato_banco(id)
    flash('Colaborador bloqueado com sucesso!', 'success')
    return redirect(url_for('contatos.listar_contatos'))

@contatos_bp.route('/agrupados-por-responsavel')
def dados_agrupados():
    # Uma tarefa com varios responsaveis aparece sob cada um deles.
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.nome AS responsavel, t.id, t.descricao, t.status, t.prazo, t.prioridade
        FROM contatos c
        INNER JOIN tarefas_contatos tc ON tc.contato_id = c.id
        INNER JOIN tarefas t ON t.id = tc.tarefa_id
        ORDER BY c.nome ASC, t.id DESC
    """)
    dados = [dict(linha) for linha in cursor.fetchall()]
    conn.close()
    for linha in dados:
        linha['status_final'] = status_efetivo(linha)
    return render_template('tarefas/quadro_admin.html', dados_agrupados=dados)

@contatos_bp.route('/filtrar-por-contato/<int:contato_id>')
def filtrar_por_contato(contato_id):
    contato = buscar_contato_por_id(contato_id)
    if not contato:
        flash('Colaborador não localizado para aplicação do filtro.', 'danger')
        return redirect(url_for('contatos.listar_contatos'))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.*
        FROM tarefas t
        INNER JOIN tarefas_contatos tc ON tc.tarefa_id = t.id
        WHERE tc.contato_id = ?
        ORDER BY t.id DESC
    """, (contato_id,))
    tarefas_filtradas = [dict(linha) for linha in cursor.fetchall()]
    conn.close()
    for tarefa in tarefas_filtradas:
        tarefa['status_final'] = status_efetivo(tarefa)
    return render_template('tarefas/quadro.html', contato=contato, tarefas=tarefas_filtradas)