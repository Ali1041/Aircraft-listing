from classifieds import models
from django.http import HttpResponse


def create_classified_abstraction(request, **kwargs):
    aircraft_type = models.AircraftType.objects.get(pk=request.POST['type'])
    aircraft_make = models.AircraftMake.objects.get(pk=request.POST['make'])
    classified_instance = models.Classified.objects.create(
        aircraft_type=aircraft_type,
        aircraft_make=aircraft_make,
        aircraft_status=kwargs['aircraft_status'][0],
        aircraft_location=kwargs['aircraft_location'][0],
        serial_number=kwargs['serial_number'][0],
        commercial_aircraft=kwargs['CA'][0],
        price_usd=kwargs['price'][0],
        year_of_make=kwargs['year'][0],

        description=kwargs['description'][0],
        engine_details=kwargs['engine_detail'][0],
        interior=kwargs['interior'][0],
        exterior=kwargs['exterior'][0],
        avionics=kwargs['avionics'][0],
        maintenance_status=kwargs['maintenance_status'][0],
        additional_information=kwargs['additional_status'][0],
        seller_email=kwargs['seller_email'][0],
        phone_number=kwargs['phone_number'][0],
        company_name=kwargs['company_name'][0],
        company_logo=request.FILES['logo'],

        user=request.user
    )
    classified_instance.aircraft_make.number_of_classifieds += 1
    classified_instance.payment_completed = False
    classified_instance.classified_status = models.Classified.AWAITING_PAYMENT
    classified_instance.save()

    for img in request.FILES.getlist('main_image'):
        models.ClassifiedImage.objects.create(
            classified=classified_instance,
            image=img
        )
    return classified_instance


def deleting_classified_abstraction(request, **kwargs):
    classified_instance = models.Classified.objects.get(pk=kwargs['pk'])
    classified_instance.delete()
    return HttpResponse(status=204)
