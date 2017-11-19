from .models import Region


def region_list(request):
    # TODO sort by buschenschank count
    return {'regions': Region.objects.all()}
