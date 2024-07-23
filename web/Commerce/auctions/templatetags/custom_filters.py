from django import template

register = template.Library()


@register.filter(name="usd")
def usd(amount: float):
    return f"${amount:.2f}"
