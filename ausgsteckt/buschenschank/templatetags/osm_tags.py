from django import template

register = template.Library()


@register.simple_tag
def osmtag(node, tagname):
    return node.tags.get(tagname)
