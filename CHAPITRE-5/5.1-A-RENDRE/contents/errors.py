from flask import flash, render_template

def get_form_errors(form):
  for _, errors in form.errors.items():
    for error in errors:
      flash(error, "danger")


def page_not_found(e):
  e.description = "La page recherchée n'existe pas ou n'a pas encore été créée."
  flash(e.description, "danger")
  return render_template("404.html")


def server_error(e):
  e.description = "Une erreur interne s'est produite."
  flash(e.description, "danger")
  return render_template("500.html")