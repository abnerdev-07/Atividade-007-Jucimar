#contatos/routes
from flask import Blueprint, render_template, request, redirect, url_for, flash
from contatos.models import (
    buscar_todos_contatos, inserir_contato_banco, email_ja_cadastrado,
    contato_possui_tarefas, remover_contato_banco, buscar_contato_por_id
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

@contatos_bp.route('/apagar/<int:id>', methods=['POST'])
def apagar_contato(id):
    if contato_possui_tarefas(id):
        flash('Ação Bloqueada! Não é permitido excluir um colaborador que possui tarefas pendentes.', 'danger')
        return redirect(url_for('contatos.listar_contatos'))
        
    remover_contato_banco(id)
    flash('Colaborador removido do sistema com sucesso!', 'success')
    return redirect(url_for('contatos.listar_contatos'))

@contatos_bp.route('/agrupados-por-responsavel')
def dados_agrupados():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.nome as responsavel, t.descricao, t.status, t.prazo, t.prioridade 
        FROM contatos c
        INNER JOIN tarefas t ON c.id = t.contato_id
        ORDER BY c.nome ASC
    """)
    dados = cursor.fetchall()
    conn.close()
    return render_template('tarefas/quadro_admin.html', dados_agrupados=dados)

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
