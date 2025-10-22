from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Récupère une valeur d'un dictionnaire par clé dans les templates"""
    return dictionary.get(key, '')