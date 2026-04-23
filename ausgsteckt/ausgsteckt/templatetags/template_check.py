import logging

from django import template
from django.template import loader

register = template.Library()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


@register.simple_tag
def template_exists(template_name):
    try:
        loader.get_template(template_name)
        return True
    except template.TemplateDoesNotExist:
        logger.debug("Template not found %s", template_name)
        return False
