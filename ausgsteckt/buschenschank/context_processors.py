from .models import Region


def region_list(request):
    regions = sorted(
        Region.objects.all(),
        key=lambda r: r.get_buschenschank().count(), reverse=True)
    return {'regions': regions}
