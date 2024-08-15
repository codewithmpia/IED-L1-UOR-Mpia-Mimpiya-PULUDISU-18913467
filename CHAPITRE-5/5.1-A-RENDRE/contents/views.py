from flask import render_template, redirect, request, url_for, flash, abort
from flask.views import MethodView
from mysql.connector import Error

from .errors import get_form_errors
from .forms import SearchForm, CommentForm
from .db import get_db_connection


class IndexView(MethodView):
  """
  Vue pour la page d'accueil.

  Cette vue charge les articles de la base de données et les rendre dans le template "index.html".
  Elle gère également la recherche d'articles en utilisant le formulaire SearchForm.
  Si aucun article n'est trouvé pour une recherche, une alerte est affichée.
  Si aucun article n'est trouvé dans la base de données pour une recherche vide, une autre alerte est affichée.
  """

  template_name = "index.html"
  form_class = SearchForm

  def get(self):
    # Instanciation du formulaire et récupération de la recherche
    form = self.form_class()
    search = request.args.get("search")

    try:
      with get_db_connection() as conn:
        cursor = conn.cursor()

        # Recherche des articles
        if search:
          cursor.execute(
            """
            SELECT * FROM posts 
            WHERE title LIKE %s OR resume LIKE %s OR content LIKE %s 
            AND publish = 1 ORDER BY created_at DESC""", 
            ("%"+search+"%", "%"+search+"%", "%"+search+"%"))
          posts = cursor.fetchall()
          
        else:
          cursor.execute("SELECT * FROM posts WHERE publish = 1 ORDER BY created_at DESC")
          posts = cursor.fetchall()
        
        # Conversion des tuples en dictionnaires
        posts = [
          dict(
            id=post[0], 
            title=post[1], 
            author=post[2], 
            resume=post[3], 
            content=post[4], 
            image=post[5], 
            views=post[6], 
            link=post[7], 
            created_at=post[8], 
            publish=post[9]
          ) for post in posts]

    except Error as e:
      abort(500)

    # Affichage d'alertes si aucun article n'est trouvé
    if not posts and search is None:
      flash("Aucun article n'est disponible pour l'instant.", "info")
    elif search is not None and not posts:
      flash("Aucun article ne correspond à votre recherche.", "info")

    return render_template(
      self.template_name, 
      posts=posts, 
      form=form, search=search)

  

class PostDetailView(MethodView):
  """
  Vue pour afficher un article en détail.
  """
  template_name = "detail.html"
  form_class = CommentForm

  def get(self, id):
    """
    Méthode pour afficher l'article en GET.
    """
    with get_db_connection() as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
      post = cursor.fetchone()

      if not post:
        abort(404)

      post = dict(
        id=post[0], 
        title=post[1], 
        author=post[2], 
        resume=post[3], 
        content=post[4], 
        image=post[5], 
        views=post[6], 
        link=post[7], 
        created_at=post[8], 
        publish=post[9]
      )
      

      cursor.execute("SELECT * FROM comments WHERE post_id = %s", (id,))
      comments = cursor.fetchall()
      comments = [
        dict(
          id=comment[0], 
          post_id=comment[1], 
          author=comment[2], 
          email=comment[3], 
          message=comment[4], 
          created_at=comment[5],
          active=comment[6]
        ) for comment in comments
      ]

    return render_template(
      self.template_name, 
      post=post, 
      comments=comments, 
      form=self.form_class())

  def post(self, id):
    """
    Méthode pour afficher l'article en POST.
    """
    with get_db_connection() as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
      post = cursor.fetchone()

      if not post:
        abort(404)
      # Conversion du tuple en dictionnaire
      post = dict(
        id=post[0], 
        title=post[1], 
        author=post[2], 
        resume=post[3], 
        content=post[4], 
        image=post[5], 
        views=post[6], 
        link=post[7], 
        created_at=post[8], 
        publish=post[9]
      )
      # Obtenir les commentaires
      cursor.execute("SELECT * FROM comments WHERE post_id = %s", (id,))
      comments = cursor.fetchall()
      comments = [
        dict(
          id=comment[0], 
          post_id=comment[1], 
          author=comment[2], 
          email=comment[3], 
          message=comment[4], 
          created_at=comment[5],
          active=comment[6]
        ) for comment in comments
      ]

      form = self.form_class()
      # Validation du formulaire
      if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        message = form.message.data
        # Créer un nouveau commentaire
        cursor.execute(
          "INSERT INTO comments (post_id, author, email, message) VALUES (%s, %s, %s, %s)", 
          (id, author, email, message)
        )
        conn.commit()
        conn.close()
        flash("Merci d'avoir commenté.", "success")
        print(post)
        return redirect(url_for("detail", id=post["id"]))

      elif form.errors:
        get_form_errors(form)

    return render_template(
      self.template_name, 
      post=post, 
      form=form,
      comments=comments)





