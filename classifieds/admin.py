# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _


from . import models


class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class ClassifiedImageInline(admin.TabularInline):
    model = models.ClassifiedImage
    extra = 0


class ClassifiedAdmin(admin.ModelAdmin):
    inlines = [ClassifiedImageInline, ]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.AircraftType)
admin.site.register(models.AircraftMake)
admin.site.register(models.Classified, ClassifiedAdmin)
admin.site.register(models.Newsletter)
