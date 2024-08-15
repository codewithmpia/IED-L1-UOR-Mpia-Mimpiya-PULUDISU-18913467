from flask_wtf import FlaskForm
from wtforms.fields import SearchField, StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class SearchForm(FlaskForm):
  search = SearchField("", render_kw={"placeholder": "taper votre recherche ici..."})


class CommentForm(FlaskForm):
  author = StringField(
    label="Notre nom", 
    validators=[DataRequired(message="Le nom est obligatoire")])
  email = EmailField(label="Votre email", 
          validators=[DataRequired(message="L'email est obligatoire"),
                      Email(message="L'email n'est pas valide")])
  message = TextAreaField(
    label="Votre message",
    validators=[DataRequired(message="Le message est obligatoire")]
  )
  submit = SubmitField(label="Soumettre")