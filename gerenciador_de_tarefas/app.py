from flask import Flask
import config
from database import init_db

app = Flask(__name__)
app.config.from_object(config)

init_db()

if __name__ == "__main__":
	app.run(debug=True)
