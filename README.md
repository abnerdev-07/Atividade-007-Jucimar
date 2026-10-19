# Gerenciador de Tarefas (Atividade 007)

To-Do List feito em Python (Flask) com SQLite, com lista de contatos e tarefas.
Cada tarefa tem descrição, prazo, prioridade e status, e pode ter *vários responsáveis*
(os contatos cadastrados). Projeto de grupo da UEA — Sistemas de Informação.

> Entrega: 19/10/2026, até as 18h.

## Funcionalidades

- *Contatos:* listar, adicionar, editar e bloquear (o contato bloqueado some das listas)
- *Tarefas:* criar, editar e excluir, com descrição, prazo, prioridade e um ou mais responsáveis
- *Quadro de tarefas* em três colunas: Para fazer, Fazendo e Concluída, cada status com uma cor
- *Tarefa atrasada:* quando o prazo venceu e a tarefa não está concluída, o cartão ganha um
  selo vermelho *Atrasada* (o atraso é calculado na hora, não fica salvo)
- *Filtro por contato* no quadro: escolha um contato e veja só as tarefas dele
- *Tela de tarefas agrupadas por responsável*, com filtros por status e por contato

## Como rodar

Pré-requisito: Python 3 instalado.


git clone https://github.com/abnerdev-07/Atividade-007-Jucimar.git
cd Atividade-007-Jucimar/gerenciador_de_tarefas

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS
pip install flask

python app.py


Depois abra no navegador:

- Tarefas: http://127.0.0.1:5000/tarefas
- Contatos: http://127.0.0.1:5000/contatos/

O banco de dados (SQLite) é criado sozinho na primeira execução.
Se o desenho das tabelas mudar, apague o arquivo .db local e rode de novo.

*Primeiro uso:* cadastre pelo menos um contato em Contatos antes de criar tarefas,
porque toda tarefa precisa de pelo menos um responsável.

## Módulos do projeto


gerenciador_de_tarefas/
├── app.py            # liga tudo: cria o Flask e registra os módulos
├── config.py         # configurações (banco, prioridades e status)
├── database.py       # conexão e criação das tabelas
├── contatos/         # módulo de contatos (models.py, routes.py)
├── tarefas/          # módulo de tarefas (models.py, routes.py)
├── templates/        # páginas HTML (Jinja2), uma pasta por módulo
├── static/css/       # estilos e cores de status
└── testar_tarefas.py # teste das funções de tarefas no banco


| Módulo | O que faz |
|--------|-----------|
| contatos | Cadastro de contatos e a tela de tarefas agrupadas por responsável |
| tarefas | Funções do banco (criar, listar, buscar, atualizar, excluir), cálculo do status "atrasada" e telas do quadro, nova tarefa e editar tarefa |
| database.py | Cria as tabelas e liga as chaves estrangeiras do SQLite |

## Banco de dados

Três tabelas:

- contatos: id, nome, e-mail, telefone, status (ativo ou bloqueado)
- tarefas: id, descrição, prazo, prioridade, status
- tarefas_contatos: liga cada tarefa aos seus responsáveis (uma tarefa pode ter vários contatos e um contato pode ter várias tarefas)

O status "atrasada" não fica salvo: é calculado na hora (prazo vencido e tarefa não concluída).

## Testes

- python testar_tarefas.py testa as funções de tarefas direto no banco (usa um banco temporário).
- O teste cruzado entre módulos, com a lista de conferência, está em docs/teste-cruzado.md.

## Equipe

| Nome | Função |
|------|--------|
| Abner Monteiro | Líder: escreve código e revisa o código dos demais integrantes |
| Anthony Figarella | Front-end: arte e visual do trabalho |
| Aline Miranda | SQL e revisão das sprints |
| Matheus Tavares | Back-end e correção de bugs |

## Organização do trabalho

- 12/10: repositório criado e colaboradores adicionados
- Cronograma: 8 sprints, de 12/10 a 19/10 (uma por dia)
- Tarefas organizadas em issues, agrupadas por milestone (uma milestone por sprint)
- Labels de módulo e de tipo criados
- Branch main protegida: só recebe código por Pull Request aprovado

## Regras do grupo

1. Crie uma branch a partir da main (nunca trabalhe direto nela).
2. Faça commits pequenos e com mensagem clara.
3. Abra um Pull Request com descrição e Closes #N (número da issue).
4. Só o líder altera database.py e app.py.

## Sobre a atividade

Enunciado: refazer o to-do list com lista de contatos; tarefas atribuídas a contatos e que podem ser
apagadas; cada tarefa com descrição, prazo, prioridade e status (a fazer, fazendo, concluída ou
atrasada, cada status com uma cor); tela para ver as tarefas com seus responsáveis; e cronograma do
projeto com as tarefas atribuídas.