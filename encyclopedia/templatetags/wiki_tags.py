import markdown

from django import template

register = template.Library()

@register.filter
def convert_markdown(value):        # custom template tag that returns the decoded markdown value for template
    return markdown.markdown(value)