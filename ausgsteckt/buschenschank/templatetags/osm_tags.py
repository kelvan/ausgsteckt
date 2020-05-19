from django import template
from django.template.loader import render_to_string

register = template.Library()

BADGE_TAGS = ['cuisine']
LIST_TAGS = ['opening_hours']


@register.simple_tag
def osmtag(node, tagname):
    return node.tags.get(tagname)


@register.filter
def format_value_list(value, tagname=None):
    """
    convert osm tag value to nice html representation
    :param value: osm tag value as ';' separated string
    :return: html
    """
    value = value.strip()
    if not value:
        return ''

    parts = [part.strip() for part in value.split(';')]

    make_badge = False
    make_list = False

    if tagname:
        make_badge = tagname in BADGE_TAGS
        make_list = tagname in LIST_TAGS

    context = {
        'values': parts,
        'make_badge': make_badge,
        'make_list': make_list}
    return render_to_string(
        'buschenschank/includes/tag_value_list.html',
        context=context)
