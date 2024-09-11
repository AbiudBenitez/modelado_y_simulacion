from django import template

register = template.Library()

@register.filter
def get_item(lista, index):
  try:
    return lista[index]
  except:
    return None