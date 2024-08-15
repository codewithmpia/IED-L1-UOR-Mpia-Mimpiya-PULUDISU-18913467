from pathlib import Path
from flask import Flask 

# Définir le chemin du répertoire courant
BASE_DIR = Path(__file__).resolve().parent

# Créer une instance de l'application Flask
app = Flask(__name__)

# Définir le secret key pour sécuriser les sessions
app.config["SECRET_KEY"] = "top secret"

# Importer la vue ChatView
from .views import ChatView

# Ajouter une route pour la page d'accueil ("/")
# La méthode "add_url_rule" est utilisée pour ajouter une route à l'application Flask
app.add_url_rule("/", view_func=ChatView.as_view("chat"))
