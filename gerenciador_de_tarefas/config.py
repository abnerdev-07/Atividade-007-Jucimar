import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR, "todo.db")

SECRET_KEY = "chave"

STATUS_OPCOES = ["fazer", "fazendo", "feito", "atrasado"]
<<<<<<< HEAD
PRIORIDADES = ["baixa", "media", "alta"]
=======
PRIORIDADES = ["baixa", "media", "alta"]
>>>>>>> 122ffedf4754eedf386ebcf447f26304f7a23146
