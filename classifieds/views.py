# -*- coding: utf-8 -*-
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
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
from django.db.models import Q,Count
from .utils import create_classified_abstraction, deleting_classified_abstraction, editing_classified_abstraction

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
    return render(request, "base.html")


# Ad post function
@login_required
def post_ad(request, **kwargs):
    editable_classified_instance = None
    if kwargs.get('pk') is not None:
        editable_classified_instance = models.Classified.objects.get(pk=kwargs.get('pk'))

    # POST request handle
    if request.method == "POST":
        if kwargs:
            editing_classified_abstraction(request, editable_classified_instance, **request.POST)
            return redirect('my_classifieds')


        # creating the db instance of form data
        else:
            create_classified_abstraction(request, **request.POST)
            return redirect('classifieds')

    # GET request handle
    context = {
        'aircraft_make': models.AircraftMake.objects.all(),
        'aircraft_type': models.AircraftType.objects.all(),
    }
    if editable_classified_instance:
        context['value'] = editable_classified_instance
        context['images'] = models.ClassifiedImage.objects.filter(classified_id=editable_classified_instance.id)

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

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data()
        if len(self.request.GET) == 1:
            ctx['search'] = self.request.GET.get('search')

        # aircraft make instance for filter
        aircraft_make_instances = models.AircraftMake.objects.annotate(count=Count('make_name')).order_by()
        print(aircraft_make_instances)
        ctx['aircraft_make_instances'] = aircraft_make_instances[:3]

        # aircraft type instance for filter
        aircraft_type_instances = models.AircraftType.objects.annotate(count=Count('type_name')).order_by()
        print(aircraft_type_instances)
        ctx['aircraft_type_instances'] = aircraft_type_instances[:3]

        # get remaining images
        # ctx['images'] = models.ClassifiedImage.objects.filter(pk=self.kwargs['pk'])
        return ctx

    def get_queryset(self):
        qs = models.Classified.objects.select_related('aircraft_make', 'aircraft_type').all()
        if len(self.request.GET) > 1:
            filtered_data = ClassifiedFilter(self.request.GET, queryset=qs)
            qs = filtered_data.qs
        if len(self.request.GET) == 1:
            qs = models.Classified.objects.filter(
                Q(aircraft_make__make_name__icontains=self.request.GET.get('search')) | Q(
                    aircraft_type__type_name__icontains=self.request.GET.get('search'))
            )

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

    return render(request, "my_classifieds.html", {'list': classifieds})


@login_required
def delete_classified(request, **kwargs):
    deleting_classified_abstraction(request, **kwargs)
    return redirect('my_classifieds')


# newsletter subscription
def newsletter(request):
    data = request.body
    parsed_data = dict(json.loads(data))
    models.Newsletter.objects.create(email=parsed_data['email'])
    return JsonResponse({'Msg': 'Updated'})


# search function
def search(request, **kwargs):
    classified_instance = models.Classified.objects.filter(
        Q(aircraft_make__make_name__icontains=request.GET.get('search')) | Q(
            aircraft_type__type_name__icontains=request.GET.get('search'))
    )

    return render(request, 'classifieds.html', {'list': classified_instance, 'search': 'search'})
