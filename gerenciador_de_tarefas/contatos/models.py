CONTATOS = [
    {"id": 1, "nome": "Matheus", "email": "matheus@email.com", "telefone": "92 99999-0001"},
    {"id": 2, "nome": "Abner", "email": "abner@email.com", "telefone": "92 99999-0002"},
    {"id": 3, "nome": "Aline", "email": "aline@email.com", "telefone": "92 99999-0003"},
    {"id": 4, "nome": "Anthony", "email": "anthony@email.com", "telefone": "92 99999-0004"},
]


def listar_contatos():
    return CONTATOS


def buscar_contato(contato_id):
    for contato in CONTATOS:
        if contato["id"] == contato_id:
            return contato
    return None


def criar_contato(nome, email=None, telefone=None):
    return {"id": 5, "nome": nome, "email": email, "telefone": telefone}


def atualizar_contato(contato_id, nome, email=None, telefone=None):
    if buscar_contato(contato_id) is None:
        return None
    return {"id": contato_id, "nome": nome, "email": email, "telefone": telefone}


def excluir_contato(contato_id):
    return buscar_contato(contato_id) is not None
