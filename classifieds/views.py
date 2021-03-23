# -*- coding: utf-8 -*-
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.views import generic
from . import models, forms
from django.conf import settings as proj_settings
from .filters import ClassifiedFilter
import json
from django.http import JsonResponse

# User model
User = get_user_model()


# contact form
def contacts(request):
    if request.method == "POST":
        form = forms.ContactForm(request.POST)

        if form.is_valid():
            # send mail
            msg_plain = render_to_string('emails/contact_form.txt')

            email = EmailMessage('Contact Form: %s' % form.cleaned_data.get("subject"), msg_plain,
                                 to=proj_settings.CONTACT_EMAILS)  # CONTACT EMAILS IS A LIST
            email.send()

            messages.success(request, 'Your message has been sent successfully. We will get in touch shortly!')
            return redirect('contacts')
        else:
            messages.warning(request, "Unable to send message.")
    else:
        form = forms.ContactForm()

    context = {
        "contact_main_email": proj_settings.CONTACT_MAIN_EMAIL,
        "contact_phone_number": proj_settings.CONTACT_PHONE_NUMBER,
        "contact_address": proj_settings.CONTACT_ADDRESS,
        "form": form,
    }

    return render(request, "contacts.html", context)


# signup page
def signup(request):
    # post request handle
    if request.method == 'POST':
        new_user = User.objects.create(email=request.POST['email'])
        new_user.set_password(request.POST['password'])
        new_user.save()
        return redirect('login')

    # render the page on get request
    return render(request, 'registration/registration_form.html')


# login page
def views_login(request):
    if request.method == 'POST':

        # authenticate if the user is signed up
        logging_user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if logging_user is not None:
            # login the user
            auth_views.auth_login(request, logging_user)
            return redirect('index')

    return render(request, 'registration/login.html')


# home page
def index(request):
    classifieds_list = models.Classified.objects.filter(classified_status=models.Classified.ACTIVE)
    aircraft_types = models.AircraftType.objects.all()
    top_brands = models.AircraftMake.objects.all()[0:10]
    classifieds_count = classifieds_list.count()

    # Pagination
    page = request.GET.get('page', 1)

    paginator = Paginator(classifieds_list, 10)
    try:
        classifieds_list = paginator.page(page)
    except PageNotAnInteger:
        classifieds_list = paginator.page(1)
    except EmptyPage:
        classifieds_list = paginator.page(paginator.num_pages)

    return render(request, "base.html", locals())


# Ad post function
@login_required
def post_ad(request, classified_id=None):

    # POST request handle
    if request.method == "POST":

        # getting all the form values
        aircraft_type = models.AircraftType.objects.get(pk=request.POST['type'])
        aircraft_make = models.AircraftMake.objects.get(pk=request.POST['make'])
        boolean_value = lambda: request.POST['CA'] == 'on'
        commercial_aircraft = boolean_value()
        price = request.POST['price']
        year = request.POST['year']
        serial_number = request.POST['serial_number']
        aircraft_status = request.POST['aircraft_status']
        description = request.POST['description']
        engine_detail = request.POST['engine_detail']
        interior = request.POST['interior']
        exterior = request.POST['exterior']
        avionics = request.POST['avionics']
        maintenance_status = request.POST['maintenance_status']
        additional_status = request.POST['additional_status']
        seller_email = request.POST['seller_email']
        phone = request.POST['phone_number']
        company_name = request.POST['company_name']
        location = request.POST['aircraft_location']
        company_logo = request.FILES['logo']

        # creating the db instance of form data
        classified_instance = models.Classified.objects.create(
            aircraft_type=aircraft_type,
            aircraft_make=aircraft_make,
            aircraft_status=aircraft_status,
            aircraft_location=location,
            serial_number=serial_number,
            commercial_aircraft=commercial_aircraft,
            price_usd=price,
            year_of_make=year,

            description=description,
            engine_details=engine_detail,
            interior=interior,
            exterior=exterior,
            avionics=avionics,
            maintenance_status=maintenance_status,
            additional_information=additional_status,
            seller_email=seller_email,
            phone_number=phone,
            company_name=company_name,
            company_logo=company_logo,

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
        return redirect('classifieds')

    # GET request handle
    context = {
        'aircraft_make': models.AircraftMake.objects.all(),
        'aircraft_type': models.AircraftType.objects.all(),
    }

    return render(request, "post_ad.html", context)


# payment function
def classified_pay(request, classified_id):
    classified = get_object_or_404(models.Classified, id=classified_id)

    return render(request, "classified_pay.html", locals())


# payment confirmation function
def classified_confirm_payment(request, classified_id):
    classified = get_object_or_404(models.Classified, id=classified_id)

    if classified.payment_completed:
        messages.success(request, "Payment has already been completed.")
    else:
        classified.payment_completed = True
        classified.classified_status = models.Classified.ACTIVE
        classified.save()

        msg_plain = render_to_string('emails/payment_completed.txt', {'domain_url': proj_settings.DOMAIN_URL})

        email_to_seller = EmailMessage('Payment Completed: %s' % classified.get_title(), msg_plain,
                                       to=[classified.seller_email])
        email_to_seller.send()

        messages.success(request, "Payment completed successfully. Your classified is now active.")

    return redirect('classified', classified_id=classified.id)


# activation function
def classified_activate(request, classified_id):
    classified = get_object_or_404(models.Classified, id=classified_id)

    if classified.classified_status == models.Classified.INACTIVE and classified.payment_completed:
        classified.classified_status = models.Classified.ACTIVE
        classified.save()

        messages.success(request, "Classified activated successfully.")
    else:
        messages.warning(request, "Unable to activate. Please contact administrator.")

    return redirect('my_classifieds')


# deactivate function
def classified_deactivate(request, classified_id):
    classified = get_object_or_404(models.Classified, id=classified_id)

    if classified.classified_status == models.Classified.ACTIVE:
        classified.classified_status = models.Classified.INACTIVE
        classified.save()

        messages.success(request, "Classified deactivated successfully.")
    else:
        messages.warning(request, "Unable to deactivate. Please contact administrator.")

    return redirect('my_classifieds')


# ads list with filtering function
class ClassifiedListView(generic.ListView):
    model = models.Classified
    template_name = 'classifieds.html'
    context_object_name = 'list'
    paginate_by = 10


    def get_queryset(self):
        qs = models.Classified.objects.select_related('aircraft_make', 'aircraft_type').all()
        if len(self.request.GET) > 1:
            filtered_data = ClassifiedFilter(self.request.GET, queryset=qs)
            qs = filtered_data.qs
        return qs


# detail view of classified item
class ClassifiedDetailView(generic.DetailView):
    model = models.Classified
    template_name = 'classified.html'
    context_object_name = 'detail'


# personal ad listing
@login_required
def my_classifieds(request):
    classifieds = models.Classified.objects.filter(user=request.user)

    return render(request, "my_classifieds.html", {'list':classifieds})


# newsletter subscription
def newsletter(request):
    data = request.body
    parsed_data = dict(json.loads(data))
    models.Newsletter.objects.create(email=parsed_data['email'])
    return JsonResponse({'Msg': 'Updated'})
