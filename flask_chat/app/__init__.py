from flask import Flask
from app.routes import bp

app = Flask(
    __name__,
    template_folder="templates",  # pasta de templates HTML
)

app.register_blueprint(bp)
