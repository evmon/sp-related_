from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from service.settings import SITE_ID


DEVELOPED_COUNTRY = ['USA', 'UK', 'Argentina']
HEIGHT_MAX = 27.2
WIDTH_MAX = 33.5
SEATS_MAX = 4

class Type(models.Model):
    name = models.CharField(max_length=200)


class Spare(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    types = models.ManyToManyField(Type)


class Color(models.Model):
    name = models.CharField(max_length=20)
    shade = models.CharField(max_length=20)
    sites = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()


class Transport(models.Model):
    title = models.CharField(max_length=200)
    spares = models.ManyToManyField(Spare)
    color = models.OneToOneField(Color, on_delete=models.CASCADE)


class Truck(Transport):
    lifting_gear = models.BooleanField(default=False)
    pallet_places = models.IntegerField(default=2)
    height = models.FloatField(default='1.0')
    width = models.FloatField(default='1.0')

    def is_reliable(self):
        return self.height <= HEIGHT_MAX and self.width <= WIDTH_MAX


class PassengerСar(Transport):
    hatch = models.BooleanField(default=False)
    seats = models.IntegerField(default=2)

    def travel_permission(self):
        return self.hatch and self.seats <= SEATS_MAX


class Client(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=100)


class Wheel(models.Model):
    name = models.CharField(max_length=200)
    transports = models.ManyToManyField(Transport)


class SpareManager(models.Manager):
    def country_uk(self):
        return Spare.objects.filter(country='UK')

    def all(self):
        return Spare.objects.order_by('-name')


class SpareProxy(Spare):
    objects = SpareManager()

    def is_dev(self):
        # is developed country
        return self.country in DEVELOPED_COUNTRY

    class Meta:
        proxy = True
        ordering = ['name', ]


class PlateNumberAbs(models.Model):
    number = models.IntegerField(default=0)
    KIEV_CODE = 'AA'
    DONETSK_CODE = 'AH'
    B1_CODE = 'B1'
    E1_CODE = 'E1'
    CIVIL_CODES = (
        (KIEV_CODE, 'Kiev'),
        (DONETSK_CODE, 'Donetsk'),
    )

    MILITARY_CODES = (
        (B1_CODE, 'Military law enforcement service of the AFU'),
        (E1_CODE, 'Military units of engineering troops of the AFU'),
    )

    class Meta:
        abstract = True


class CivilNumber(PlateNumberAbs):
    serial = models.CharField(
        max_length=2,
        choices=PlateNumberAbs.CIVIL_CODES,
        default=PlateNumberAbs.KIEV_CODE
    )

    def get_plate_number(self):
        return f'{self.serial}{self.number}'


class MilitaryNumber(PlateNumberAbs):
    serial = models.CharField(
        max_length=2,
        choices=PlateNumberAbs.MILITARY_CODES,
        default=PlateNumberAbs.E1_CODE
    )

    def get_plate_number(self):
        return f'{self.number} {self.serial}'

class New(models.Model):
    title = models.CharField(max_length=200)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    objects = models.Manager()
    on_site = CurrentSiteManager()
