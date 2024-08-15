from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash
from flask.views import MethodView
from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_pymongo import PyMongo


app = Flask(__name__)
app.secret_key = "top secret"

# Configuration de MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/bonus"
mongo = PyMongo(app)


class ContactForm(FlaskForm):
    """
    Formulaire de contact.
    """
    name = StringField(
        label="Votre nom",
        validators=[
            DataRequired(message="Le champs nom est obligatoire")
        ]
    )
    email = EmailField(
        label="Votre email",
        validators=[
            DataRequired(message="Le champs email est obligatoire"),
            Email(message="Veuillez entrer une adresse email valide")
        ]
    )
    subject = SelectField(
        label="A quel sujet ?",
        choices=[
            ("web", "Réaliser un projet web"),
            ("bug", "Signaler un bug"),
            ("admin", "Administrer un parc informatique")
        ],
        coerce=str
    )
    date = DateField(
        label="Quand ?",
        format="%Y-%m-%d",
        validators=[
            DataRequired(message="Le champs date est obligatoire")
        ]
    )
    message = TextAreaField(
        label="Votre message",
        validators=[
            DataRequired(message="Le champs message est obligatoire")
        ]
    )
    submit = SubmitField("Envoyer")


class IndexView(MethodView):
    """
    Vue pour la page d'accueil.
    """
    template_name = "index.html"
    form_class = ContactForm

    def get(self):
        """
        Méthode pour la requête GET.
        """
        form = self.form_class()
        # Récupérer les contacts et les trier en ordre décroissant par rapport à la date
        contacts = list(mongo.db.contacts.find().sort("date", -1))

        if len(contacts) < 1:
            flash("Il n'y a aucun contact pour le moment.", "info")
        return render_template(self.template_name, form=form, contacts=contacts)
    
    def post(self):
        """
        Méthode pour la requête POST.
        """
        form = self.form_class()

        if form.validate_on_submit():
            # Si le formulaire est valide, enregistrer les données dans la base de données
            mongo.db.contacts.insert_one({
                "name": form.name.data,
                "email": form.email.data,
                "subject": form.subject.data,
                "date": datetime.combine(form.date.data, datetime.min.time()),
                "message": form.message.data
            })
            flash("Votre message a été prise en compte.", "success")
            return redirect(url_for("index"))

        elif form.errors:
            # Si le formulaire a des erreurs, afficher les erreurs
            for _, erreors in form.errors.items():
                for error in erreors:
                    flash(error, "danger")
        return render_template(self.template_name, form=form)
    

app.add_url_rule("/", view_func=IndexView.as_view("index"))

# Lancer le serveur de devlopement
if __name__ == "__main__":
    app.run(debug=True)
