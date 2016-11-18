from django import template

register = template.Library()

ADDR_TAGS = {
    'wanted': (
        'addr:housenumber', 'addr:city', 'addr:country', 'addr:postcode'
    ),
    'anyof': (
        ('addr:street', 'addr:place'),
    )
}
CONTACT_TAGS = {
    'wanted': (
        'contact:phone', 'contact:email',
    ),
    'anyof': (
        ('website', 'contact:website'),
    )
}


def calculate_coverage(tags, tags_target):
    covered = 0
    min_tags_count = (
        len(tags_target.get('wanted', [])) + len(tags_target.get('anyof', []))
    )
    if min_tags_count == 0:
        return 1.0

    for tag_wanted in tags_target.get('wanted', []):
        if tag_wanted in tags:
            covered += 1

    for tag_anyof in tags_target.get('anyof', []):
        for tag in tag_anyof:
            if tag in tags:
                covered += 1
                break

    return min(1.0, covered/min_tags_count)


@register.simple_tag
def address_coverage(tags, percentage=False):
    coverage = calculate_coverage(tags, ADDR_TAGS)
    if percentage:
        coverage *= 100
    return round(coverage, 1)


@register.simple_tag
def contact_coverage(tags, percentage=False):
    coverage = calculate_coverage(tags, CONTACT_TAGS)
    if percentage:
        return round(coverage*100, 1)
    return round(coverage, 3)
