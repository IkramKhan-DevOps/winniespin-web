from django.core.exceptions import ValidationError
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=2, unique=True, help_text='ISO 3166-1 alpha-2')
    language = models.CharField(max_length=3, default='en', help_text='ISO 639-1', null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD', help_text='ISO 4217', null=True, blank=True)
    phone_code = models.CharField(max_length=4, default='+1', help_text='e.g. +1', null=True, blank=True)

    is_services_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=100, help_text='Application name', default='Winnie Spin')
    short_name = models.CharField(max_length=10, help_text='Your application short name', default='WS')
    tagline = models.CharField(
        max_length=100, help_text='Your application business line', default='Win big, live larger.'
    )
    description = models.TextField(
        default="At Winnie Spin, we believe in turning dreams into reality with every spin. Prepare yourself for an exhilarating journey where luck reigns supreme and winning big is not just a possibility, but a promise.",
        help_text='Application description'
    )

    favicon = models.ImageField(
        upload_to='core/application/images', null=True, blank=True, help_text='Application favicon'
    )
    logo = models.ImageField(
        upload_to='core/application/images', null=True, blank=True,
        help_text='Application real colors logo'
    )
    logo_dark = models.ImageField(
        upload_to='core/application/images', null=True, blank=True, help_text='For dark theme only'
    )
    logo_light = models.ImageField(
        upload_to='core/application/images', null=True, blank=True, help_text='For light theme only'
    )

    contact_email1 = models.EmailField(
        max_length=100, default='support@winniespin.com', help_text='Application contact email 1'
    )
    contact_email2 = models.EmailField(
        max_length=100, default='support@winniespin.com', help_text='Application contact email 2'
    )
    contact_phone1 = PhoneNumberField(
        help_text='Application contact phone 1', default='+923337800652'
    )
    contact_phone2 = PhoneNumberField(
        help_text='Application contact phone 2', default='+923337800652'
    )

    address = models.CharField(
        max_length=255, help_text='office address', default='Sarafa abazar Quetta, Balochistan Pakistan'
    ),
    latitude = models.DecimalField(max_digits=30, decimal_places=20, help_text='latitude', default=30.19759544211215)
    longitude = models.DecimalField(max_digits=30, decimal_places=20, help_text='longitude', default=67.0146412275273)

    terms_url = models.URLField(
        max_length=255, default='https://winniespin.com/terms/', help_text='Terms and Conditions page link'
    )

    version = models.CharField(max_length=10, help_text='Current version', default='1.0.0')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Application"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self,  *args, **kwargs):
        if Application.objects.exists() and not self.pk:
            raise ValidationError("Only one record allowed.")
        super(Application, self).save(*args, **kwargs)


