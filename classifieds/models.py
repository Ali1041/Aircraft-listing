# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class AircraftMake(models.Model):
    make_name = models.CharField(max_length=255)
    number_of_classifieds = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering = ['-number_of_classifieds']

    def __unicode__(self):
        return self.make_name

    @staticmethod
    def calculate_number_of_classifieds():
        for make in AircraftMake.objects.all():
            make.number_of_classifieds = Classified.objects.filter(aircraft_make=make).count()
            make.save()


class AircraftType(models.Model):
    type_make = models.ForeignKey('AircraftMake', on_delete=models.CASCADE)
    type_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.type_name


class Classified(models.Model):
    PARKED = 1
    IN_STORAGE = 2
    AIRWORTHY = 3

    AIRCRAFT_STATUS_CHOICES = (
        (PARKED, 'Parked'),
        (IN_STORAGE, 'In Storage'),
        (AIRWORTHY, 'Airworthy'),
    )

    ACTIVE = 1
    INACTIVE = 2
    AWAITING_PAYMENT = 3

    CLASSIFIED_STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (AWAITING_PAYMENT, 'Awaiting Payment'),
    )

    COMMERCIAL_AIRCRAFT_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )

    YEAR_CHOICES = []
    for r in range(1960, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True, editable=False)
    classified_status = models.IntegerField(choices=CLASSIFIED_STATUS_CHOICES, default=ACTIVE)
    payment_completed = models.BooleanField(default=True)

    price_usd = models.DecimalField(max_digits=8, decimal_places=2)
    aircraft_type = models.ForeignKey(AircraftType, on_delete=models.CASCADE)
    aircraft_make = models.ForeignKey(AircraftMake, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    year_of_make = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    aircraft_status = models.IntegerField(choices=AIRCRAFT_STATUS_CHOICES, default=PARKED)
    commercial_aircraft = models.BooleanField(default=False, choices=COMMERCIAL_AIRCRAFT_CHOICES)
    description = models.TextField(blank=True, null=True)
    engine_details = models.TextField(blank=True, null=True)
    interior = models.TextField(blank=True, null=True)
    exterior = models.TextField(blank=True, null=True)
    avionics = models.TextField(blank=True, null=True)
    maintenance_status = models.TextField(blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)

    phone_number = models.CharField(max_length=20)
    seller_email = models.EmailField()
    aircraft_location = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_logo = models.ImageField(blank=True, null=True, upload_to='company_logos')

    class Meta:
        ordering = ['-date_time']

    def __unicode__(self):
        return self.get_title()

    @staticmethod
    def get_max_price():
        return 5000000

    def get_title(self):
        commercial_str = ""

        if self.commercial_aircraft:
            commercial_str = "Commercial"

        return "%s %s For Sale %s %s ($ %s)" % (
            commercial_str, self.aircraft_type.type_name, self.aircraft_make.make_name, self.year_of_make,
            self.price_usd)

    def get_images(self):
        return ClassifiedImage.objects.filter(classified=self)

    def get_images_count(self):
        return ClassifiedImage.objects.filter(classified=self).count()

    def get_main_image(self):
        images = ClassifiedImage.objects.filter(classified=self)

        if images.count() == 0:
            return False
        else:
            return images.first()


class ClassifiedImage(models.Model):
    classified = models.ForeignKey(Classified, on_delete=models.CASCADE)
    image = ImageField(upload_to="classified_images")

    # def __unicode__(self):
    #     return "Image for classified #s" % (str(self.classified.id),)
