from . import models


def categories_processor(request):
    categories = models.AircraftType.objects.all()

    return locals()