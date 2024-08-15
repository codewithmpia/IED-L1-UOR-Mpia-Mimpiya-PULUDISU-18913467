"""
Exercice 7.2 (Mini-Projet - à Rendre)

CHATBOT 

Avant de lancer ce mini-chatbot, il faut commencer par:

- Créer un environnement virtuel:
    python -m venv venv ou python3 -m venv venv

- Activer l'environnement virtuel:
    source venv/bin/activate

- Installer les modules:
    pip install -r requirements.txt ou pip3 install -r requirements.txt

- Lancer le mini-chatbot:
    python run.py ou python3 run.py
"""

from contents.settings import app


if __name__ == "__main__":
    app.run(debug=True)