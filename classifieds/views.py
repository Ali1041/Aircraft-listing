# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from . import models, forms
from django.conf import settings as proj_settings



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
        logging_user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if logging_user is not None:
            # login the user
            auth_views.auth_login(request, request.POST['username'])
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


def classified(request, classified_id):
    classified = get_object_or_404(models.Classified, id=classified_id)

    if request.method == "POST":
        form = forms.ContactSellerForm(request.POST)

        if form.is_valid():
            msg_plain = render_to_string('emails/contact_seller.txt', {'domain_name': proj_settings.DOMAIN_NAME,
                                                                       "name": form.cleaned_data.get("name"),
                                                                       "email": form.cleaned_data.get("email"),
                                                                       "phone": form.cleaned_data.get("phone"),
                                                                       "message": form.cleaned_data.get("message")
                                                                       })

            email_to_seller = EmailMessage('Inquiry about: %s' % classified.get_title(), msg_plain,
                                           to=[form.cleaned_data.get("email")])
            email_to_seller.send()

            messages.add_message(request, messages.SUCCESS, "Message Sent!")
            return redirect('classified', classified_id=classified.id)
        else:
            messages.warning(request, "Unable to send message")
    else:
        form = forms.ContactSellerForm()

    context = {
        "classified": classified,
        "form": form
    }

    return render(request, "classified.html", context)


# Ad post function
@login_required
def post_ad(request, classified_id=None):
    extra = 1

    classified_instance = None
    images_queryset = models.ClassifiedImage.objects.none()

    if classified_id is not None:
        classified_instance = get_object_or_404(models.Classified, id=classified_id)
        images_queryset = models.ClassifiedImage.objects.filter(classified=classified_instance)

    ClassifiedImageFormset = modelformset_factory(models.ClassifiedImage, form=forms.ClassifiedImageForm,
                                                  exclude=('classified',), extra=extra, can_delete=True)

    if request.method == "POST":
        raise ValueError('In development')
        form = forms.ClassifiedForm(request.POST, request.FILES, instance=classified_instance)
        images_formset = ClassifiedImageFormset(request.POST, request.FILES)

        if form.is_valid() and images_formset.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.payment_completed = False
            ad.classified_status = models.Classified.AWAITING_PAYMENT
            ad.save()

            # update aircraft make count
            ad.aircraft_make.number_of_classifieds += 1
            ad.aircraft_make.save()

            # save the images in formset
            images_formset.save(commit=False)
            for images_form in images_formset:
                if images_form.has_changed():
                    obj = images_form.save(commit=False)
                    obj.classified = ad
                    obj.save()

            if classified_instance is None:
                # Send confirmation email
                msg_plain = render_to_string('emails/ad_created.txt', {'domain_url': proj_settings.DOMAIN_URL})

                email_to_seller = EmailMessage('Classified created: %s' % ad.get_title(), msg_plain,
                                               to=[ad.seller_email])
                email_to_seller.send()

                # redirect to pay for classified view
                messages.success(request, "Classified has been created successfully. Please complete the payment.")
                return redirect('classified_pay', classified_id=ad.id)
            else:
                # redirect to view classified
                messages.success(request, "Your classified has been successfully edited.")
                return redirect('classified', classified_id=ad.id)
        else:
            messages.warning(request, "Unable to create classified. Please check if the form is correct.")
    else:
        form = forms.ClassifiedForm(instance=classified_instance)
        images_formset = ClassifiedImageFormset(queryset=images_queryset)

    context = {
        "form": form,
        "images_formset": images_formset,
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
def classifieds(request):
    form = forms.SearchForm(request.GET)
    classifieds_list = models.Classified.objects.filter(classified_status=models.Classified.ACTIVE)

    # Filtering
    if 'aircraft_type' in request.GET and request.GET.get('aircraft_type'):
        categories_ids = [int(i) for i in request.GET.getlist('aircraft_type')]
        classifieds_list = classifieds_list.filter(aircraft_type__id__in=categories_ids)

    if 'aircraft_make' in request.GET:
        make_ids = [int(i) for i in request.GET.getlist('aircraft_make')]
        classifieds_list = classifieds_list.filter(aircraft_make__id__in=make_ids)

    if 'max_price' in request.GET and request.GET.get('max_price'):
        max_price = request.GET.get('max_price')
        classifieds_list = classifieds_list.filter(price_usd__lte=Decimal(max_price))

    if 'min_price' in request.GET and request.GET.get('min_price'):
        max_price = request.GET.get('min_price')
        classifieds_list = classifieds_list.filter(price_usd__gte=Decimal(max_price))

    if 'max_year' in request.GET and request.GET.get('max_year'):
        max_price = request.GET.get('max_year')
        classifieds_list = classifieds_list.filter(year_of_make__lte=int(max_price))

    if 'min_year' in request.GET and request.GET.get('min_year'):
        max_price = request.GET.get('min_year')
        classifieds_list = classifieds_list.filter(year_of_make__gte=int(max_price))

    if 'sort_by' in request.GET and request.GET.get('sort_by'):
        sort_by = request.GET.get('sort_by')
        # print sort_by

        if sort_by == "updated":
            classifieds_list = classifieds_list.order_by('-date_time')
        elif sort_by == "price":
            classifieds_list = classifieds_list.order_by('price_usd')

    # Pagination
    page = request.GET.get('page', 1)

    paginator = Paginator(classifieds_list, 10)
    try:
        classifieds_list = paginator.page(page)
    except PageNotAnInteger:
        classifieds_list = paginator.page(1)
    except EmptyPage:
        classifieds_list = paginator.page(paginator.num_pages)

    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()

    return render(request, "classifieds.html", {"classifieds_list": classifieds_list,
                                                "max_price": models.Classified.get_max_price(),
                                                "form": form,
                                                "page": paginator,
                                                "parameters": parameters})


# personal ad listing
@login_required
def my_classifieds(request):
    classifieds = models.Classified.objects.filter(user=request.user)

    return render(request, "my_classifieds.html", locals())
