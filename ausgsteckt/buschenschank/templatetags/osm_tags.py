from urllib.parse import urlparse

from django import template
from django.template.loader import render_to_string

register = template.Library()

BADGE_TAGS = ["cuisine"]
LIST_TAGS = ["opening_hours"]

SAFE_URL_SCHEMES = {"http", "https"}


@register.simple_tag
def osmtag(node, tagname):
    return node.tags.get(tagname)


@register.filter
def external_url(value):
    """
    Return an osm tag value only if it is a safe http(s) URL, otherwise "".

    Tag values are contributed by anyone editing OpenStreetMap, so a value
    like ``contact:facebook=javascript:alert(1)`` would end up in an href and
    execute when clicked. Autoescaping does not prevent this, it escapes the
    value but not the URL scheme.
    """
    if not value:
        return ""

    url = str(value).strip()
    if not url:
        return ""

    parsed = urlparse(url)
    if not parsed.scheme and not url.startswith("//"):
        # bare domain such as "example.com/page"
        url = f"http://{url}"
        parsed = urlparse(url)

    if parsed.scheme not in SAFE_URL_SCHEMES or not parsed.netloc:
        return ""

    return url


@register.filter
def format_value_list(value, tagname=None):
    """
    convert osm tag value to nice html representation
    :param value: osm tag value as ';' separated string
    :return: html
    """
    value = value.strip()
    if not value:
        return ""

    parts = [part.strip() for part in value.split(";")]

    make_badge = False
    make_list = False

    if tagname:
        make_badge = tagname in BADGE_TAGS
        make_list = tagname in LIST_TAGS

    context = {"values": parts, "make_badge": make_badge, "make_list": make_list}
    return render_to_string("buschenschank/includes/tag_value_list.html", context=context)
