import json
from flask import render_template, request, jsonify
from flask.views import MethodView

from .settings import BASE_DIR
from .chat import model, predict_class, get_response

class ChatView(MethodView):
    """
    Vue pour gérer les requêtes GET et POST du chatbot.
    """
    template_name = "chat.html"
    intents = json.loads(open(f"{BASE_DIR}/intents.json").read())

    def get(self):
        """
        Requête GET : Renvoie le template HTML du chatbot.
        """
        return render_template(self.template_name)
    
    def post(self):
        """
        Requête POST : Renvoie la réponse du chatbot en fonction du message envoyé.
        """
        # Récupère le message envoyé
        message = request.get_json()["message"]

        # Si le message est vide, renvoie une erreur
        if not message:
            return jsonify({"error": "Pas de message"}), 400

        # Prédit l'intention du message
        ints = predict_class(message, model)

        # Renvoie la réponse correspondante
        response = get_response(ints, self.intents)
        return jsonify({"response": response})
