from django import template

register = template.Library()


@register.filter
def clp(valor):
    """Formatea un entero como precio chileno: 35000 -> '35.000'."""
    return f'{int(valor):,}'.replace(',', '.')


@register.filter
def estrellas(valor):
    """Convierte una calificación promedio en estrellas: 4.2 -> '★★★★☆'."""
    if not valor:
        return ''
    llenas = int(round(valor))
    return '★' * llenas + '☆' * (5 - llenas)
