import markdown
from pygments.formatters import HtmlFormatter



def format_markdown(object):
    # Transforme le texte en Markdown
    md_template_string = markdown.markdown(object, extensions=["fenced_code", "codehilite"])
    # Crée un formatteur pour le CSS des blocs de code syntaxiquement étiquetés
    formatter = HtmlFormatter(style="vim", full=True, cssclass="codehilite")
    # Récupère la chaîne de caractères CSS
    css_string = formatter.get_style_defs()
    # Crée une balise <style> contenant les CSS récupérés
    md_css_string = "<style>" + css_string + "</style>"
    # Concatène le CSS avec le template Markdown pour former le rendu final
    md_template = md_css_string + md_template_string
    return md_template

def pluralize(object, singular="", plural="s"):
    """
    Retourne le mot adéquat pour indiquer que le nombre d'éléments
    dans object est singulier ou pluriel.
    """
    if len(object) <= 1:
        return singular
    return plural

