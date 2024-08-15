from flask import Flask
from flask_minify import Minify

from .import utils
from .filters import format_markdown, pluralize
from .errors import page_not_found, server_error

# Initialisation de l'application
app = Flask(
  __name__,
  template_folder=utils.TEMPLATE_DIR,
  static_folder=utils.STATIC_DIR
)

# Secret key
app.config["SECRET_KEY"] = utils.get_env_vars("SECRET_KEY", utils.DEV_KEY)

# Gestion de cookie
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True


# Minify
Minify(app=app, html=True, js=True, cssless=True)

# Custom template filters
app.add_template_filter(format_markdown, name="format_md")
app.add_template_filter(pluralize, "pluralize")

# Errors Handlers
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, server_error)

# Routes
from .views import IndexView, PostDetailView

app.add_url_rule("/", view_func=IndexView.as_view("index"))
app.add_url_rule("/posts/<int:id>/", view_func=PostDetailView.as_view("detail"))
