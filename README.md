# Gerenciador de Tarefas (Atividade 007)

To-Do List feito em Python (Flask) com SQLite, com lista de contatos e tarefas.
Cada tarefa tem descrição, prazo, prioridade e status, e pode ter **vários responsáveis**
(os contatos cadastrados). Projeto de grupo da UEA — Sistemas de Informação.

> Status do projeto: em desenvolvimento. Entrega em 19/10/2026, até as 18h.

## Funcionalidades

- Cadastro de contatos (listar, adicionar, editar e apagar)
- Cadastro de tarefas com um ou mais responsáveis
- Status: a fazer, fazendo, concluída e atrasada (cada um com uma cor)
- Apagar tarefa
- Contato que ainda tem tarefa não pode ser apagado (é preciso reatribuir antes)
- Tela que mostra as tarefas agrupadas por responsável

## Como rodar

Pré-requisito: Python 3 instalado.

```
git clone https://github.com/[usuario]/Atividade-007-Jucimar.git
cd Atividade-007-Jucimar/gerenciador_de_tarefas

python -m venv venv
venv\Scripts\activate          # Windows
pip install flask

python app.py
```

Depois abra no navegador: http://127.0.0.1:5000

O banco de dados (SQLite) é criado sozinho na primeira execução.
Se o desenho das tabelas mudar, apague o arquivo `.db` local e rode de novo.

## Estrutura do projeto

```
gerenciador_de_tarefas/
├── app.py            # liga tudo: cria o Flask e registra os módulos
├── config.py         # configurações (caminho do banco)
├── database.py       # conexão e criação das tabelas
├── contatos/         # módulo de contatos (models.py, routes.py)
├── tarefas/          # módulo de tarefas (models.py, routes.py, status.py)
├── templates/        # páginas HTML (Jinja2)
└── static/css/       # estilos e cores de status
```

## Banco de dados

Três tabelas:

- `contatos`: id, nome, e-mail, telefone
- `tarefas`: id, descrição, prazo, prioridade, status
- `tarefas_contatos`: liga cada tarefa aos seus responsáveis (uma tarefa pode ter vários contatos e um contato pode ter várias tarefas)

O status "atrasada" não fica salvo: é calculado na hora (prazo vencido e tarefa não concluída).

## Equipe

| Nome | Função |
|------|--------|
| Abner Monteiro | Líder: escreve codigo e faz revisão dos codigos do demais integrantes. |
| Anthony Figarella | cuida do front-end da arte e do visual do nosso trabalho.|
| Aline Miranda | mexe no SQL e revisão das sprints | 
| Mathesu Tavares | back-end e corrige bugs|

## Organização do trabalho

- 12/10: repositório criado e colaboradores adicionados
- Cronograma: 8 sprints, de 12/10 a 19/10 (uma por dia)
- Tarefas organizadas em issues, agrupadas por milestone (uma milestone por sprint)
- Labels de módulo e de tipo criados
- Branch `main` protegida: só recebe código por Pull Request aprovado

## Regras do grupo

1. Crie uma branch a partir da `main` (nunca trabalhe direto nela).
2. Faça commits pequenos e com mensagem clara.
3. Abra um Pull Request com descrição e `Closes #N` (número da issue).
4. Só o líder altera `database.py` e `app.py`.

## Sobre a atividade

Enunciado: refazer o to-do list com lista de contatos; tarefas atribuídas a contatos e que podem ser
apagadas; cada tarefa com descrição, prazo, prioridade e status (a fazer, fazendo, concluída ou
atrasada, cada status com uma cor); tela para ver as tarefas com seus responsáveis; e cronograma do
projeto com as tarefas atribuídas.

