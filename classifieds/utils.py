from classifieds import models
from django.http import HttpResponse


def create_classified_abstraction(request, **kwargs):
    aircraft_type = models.AircraftType.objects.get(pk=['type'])
    aircraft_make = models.AircraftMake.objects.get(pk=['make'])
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


def editing_classified_abstraction(request, editable_classified_instance, **kwargs):
    aircraft_type = models.AircraftType.objects.get(pk=['type'])
    aircraft_make = models.AircraftMake.objects.get(pk=['make'])
    company_logo = request.FILES.get('logo')
    editable_classified_instance.aircraft_status = kwargs['aircraft_status'][0]
    editable_classified_instance.aircraft_type = aircraft_type
    editable_classified_instance.aircraft_make = aircraft_make
    editable_classified_instance.serial_number = kwargs['serial_number'][0]
    editable_classified_instance.commercial_aircraft = kwargs['CA'][0]
    editable_classified_instance.price_usd = kwargs['price'][0]
    editable_classified_instance.year_of_make = kwargs['year'][0]
    editable_classified_instance.description = kwargs['description'][0]
    editable_classified_instance.engine_details = kwargs['engine_detail'][0]
    editable_classified_instance.interior = kwargs['interior'][0]
    editable_classified_instance.exterior = kwargs['exterior'][0]
    editable_classified_instance.avionics = kwargs['avionics'][0]
    editable_classified_instance.maintenance_status = kwargs['maintenance_status'][0]
    editable_classified_instance.additional_information = kwargs['additional_status'][0]
    editable_classified_instance.phone_number = kwargs['phone_number'][0]
    editable_classified_instance.seller_email = kwargs['seller_email'][0]
    editable_classified_instance.company_name = kwargs['company_name'][0]
    editable_classified_instance.aircraft_location = kwargs['aircraft_location'][0]

    main_images = request.FILES.getlist('main_images')
    if main_images:
        classified_images_instance = models.ClassifiedImage.objects.filter(
            classified_pk=editable_classified_instance.pk)
        for img in range(0, len(classified_images_instance)):
            if len(main_images) <= img:
                classified_images_instance[img].image = main_images[img]
            else:
                classified_images_instance[img].delete()

    if company_logo:
        editable_classified_instance.company_logo = company_logo
    else:
        editable_classified_instance.company_logo = editable_classified_instance.company_logo

    editable_classified_instance.save()
    return editable_classified_instance
