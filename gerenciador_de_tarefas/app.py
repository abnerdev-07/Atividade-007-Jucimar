from flask import Flask
import config
from database import init_db
from contatos.routes import contatos_bp

app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(contatos_bp)

init_db()

if __name__ == "__main__":
    app.run(debug=True)