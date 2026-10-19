# Teste cruzado entre os módulos (S7)

Cada módulo é testado por **alguém diferente do autor**. O testador segue a lista, marca `[x]`
no que passou e anota o problema no que falhou. Quem achar erro abre uma **issue** com o label `bug`
(descreve o passo, o que esperava e o que aconteceu).

Pronto quando: todos os módulos abaixo tiverem a coluna **Testador** preenchida (nome diferente do
autor) e todos os itens marcados `[x]` ou com issue aberta.

## Quem testa quem

| Módulo | Autor | Testador | Resultado (OK / bugs: #issue) | Data |
|--------|-------|----------|-------------------------------|------|
| A. Contatos | | | | |
| B. Tarefas (criar, editar, excluir) | | | | |
| C. Status e atrasada | | | | |
| D. Tela de tarefas (quadro e filtro) | | | | |
| E. Instalação e README | | | | |

Regra: testador ≠ autor. Se não souber quem fez o quê, veja o autor do último commit
do arquivo no GitHub (`git log -- <arquivo>`).

## Preparação (todo testador, antes de começar)

1. Estar na `main` atualizada (GitHub Desktop → Fetch origin → Pull origin).
2. Ambiente virtual ativo e `pip install flask`.
3. **Apagar o arquivo `.db` local** para começar com banco limpo (o schema mudou várias vezes).
4. `python app.py` e abrir http://127.0.0.1:5000

## A. Contatos

Rotas: `/contatos/`, `/contatos/novo`, `/contatos/editar/<id>`

- [ ] Abrir `/contatos/` sem contatos: a página abre sem erro.
- [ ] Criar contato com nome, e-mail e telefone: aparece na lista e a mensagem de sucesso aparece.
- [ ] Criar contato **sem nome** ou **sem e-mail**: mostra erro e não cria.
- [ ] Criar contato com **e-mail repetido**: mostra erro e não cria.
- [ ] Editar um contato (trocar o nome): a lista mostra o nome novo.
- [ ] Editar usando o e-mail de **outro** contato: mostra erro. Editar mantendo o próprio e-mail: funciona.
- [ ] Bloquear (apagar) um contato **sem tarefas**: ele some da lista.
- [ ] Bloquear um contato **com tarefas**: o sistema se comporta como o grupo decidiu
      (impede e avisa, ou libera as tarefas). Anotar qual regra está valendo: ______
- [ ] Contato bloqueado **não aparece** no formulário de nova tarefa nem no filtro.

## B. Tarefas (criar, editar, excluir)

Rotas: `/tarefas/nova`, `/tarefas/<id>/editar`, botão Excluir

- [ ] Criar tarefa com descrição, prazo, prioridade, status e **um** responsável: aparece no quadro.
- [ ] Criar tarefa com **dois ou mais** responsáveis: todos aparecem (avatares) no cartão.
- [ ] Criar tarefa **sem descrição**: mostra erro e não cria.
- [ ] Criar tarefa **sem responsável**: mostra erro e não cria.
- [ ] Criar tarefa **sem prazo**: cria e o cartão mostra "Sem prazo".
- [ ] Editar a descrição, a prioridade e o status: as mudanças aparecem no quadro.
- [ ] Editar trocando o responsável (tirar um e marcar outro): o quadro mostra o novo.
- [ ] Excluir uma tarefa (botão Excluir, confirmar): ela some e o banco não dá erro.
- [ ] Cancelar a confirmação de excluir: a tarefa continua lá.
- [ ] Abrir `/tarefas/9999/editar` (id que não existe): mostra "não encontrado" (404), sem erro de servidor.

## C. Status e atrasada

- [ ] Tarefa com status "fazer" e prazo **futuro**: coluna Para fazer, **sem** selo vermelho.
- [ ] Tarefa com status "fazer" e prazo **vencido** (ex.: 01/10/2026): coluna Para fazer com selo vermelho **Atrasada**.
- [ ] Tarefa "fazendo" com prazo vencido: coluna Fazendo, com selo vermelho.
- [ ] Tarefa "concluída" com prazo vencido: coluna Concluída, **sem** selo vermelho.
- [ ] Tarefa de prazo **hoje**: **não** é atrasada (só vence no dia seguinte).
- [ ] Tarefa sem prazo: nunca fica atrasada.
- [ ] Cada status tem uma cor diferente (fazer, fazendo, concluída, atrasada).
- [ ] Rodar `python testar_tarefas.py`: todos os testes passam (sem `FAIL`).

## D. Tela de tarefas (quadro e filtro)

Rotas: `/tarefas`, `/tarefas?contato=<id>`, `/contatos/agrupados-por-responsavel`

- [ ] `/tarefas` mostra as colunas com contador certo (número de cartões = número no contador).
- [ ] Filtrar por um contato no menu: só as tarefas dele aparecem.
- [ ] Contato **sem tarefas** no filtro: mostra "Este contato não tem tarefas.".
- [ ] "Limpar filtro" volta a mostrar todas as tarefas.
- [ ] Tarefa com 2 responsáveis aparece no filtro dos **dois**.
- [ ] `/tarefas?contato=9999` (contato que não existe): não quebra a página.
- [ ] `/contatos/agrupados-por-responsavel` abre e mostra as tarefas agrupadas por responsável.
- [ ] Os links (+ Nova tarefa, Editar tarefa, menu) levam para a página certa.

## E. Instalação e README (alguém que nunca rodou o projeto)

- [ ] Clonar o repositório **em uma pasta nova** (não usar a pasta de trabalho).
- [ ] Seguir **só o README**: criar venv, `pip install flask`, `python app.py`.
- [ ] O app abre em http://127.0.0.1:5000 sem erro.
- [ ] O banco é criado sozinho na primeira execução.
- [ ] O README tem nomes e funções dos 4 integrantes, sem `[preencher]`.
- [ ] O README descreve o que o sistema faz e bate com o que existe de verdade.
- [ ] Não há arquivos soltos no repositório (`.save`, `__pycache__`, `.db`, `venv`).

## Registro de bugs encontrados

| # | Módulo | O que aconteceu | Issue | Corrigido? |
|---|--------|-----------------|-------|------------|
| 1 | | | | |
| 2 | | | | |