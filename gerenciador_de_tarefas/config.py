import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR, "todo.db")

SECRET_KEY = "chave"

STATUS_OPCOES = ["fazer", "fazendo", "concluida"]
PRIORIDADES = ["baixa", "media", "alta"]