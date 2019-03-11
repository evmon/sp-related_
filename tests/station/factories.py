import factory

from station.models import (Spare, Transport, Client, Type, Color, Wheel,
    Truck, PassengerСar, CivilNumber, MilitaryNumber, )


class SpareFactory(factory.django.DjangoModelFactory):
    country = "USA"
    name = "Head Lights"

    class Meta:
        model = Spare


class TransportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transport


class MilitaryNumberFactory(factory.django.DjangoModelFactory):
    number = '9990'
    class Meta:
        model = MilitaryNumber


class CivilNumberFactory(factory.django.DjangoModelFactory):
    number = '6572'
    class Meta:
        model = CivilNumber


class TruckFactory(factory.django.DjangoModelFactory):
    lifting_gear = False
    pallet_places = 2
    width = 12.3
    height = 11.1

    class Meta:
        model = Truck


class PassengerСarFactory(factory.django.DjangoModelFactory):
    hatch = True
    seats = 4

    class Meta:
        model = PassengerСar


class ClientFactory(factory.django.DjangoModelFactory):
    name = "Evheniya Monastyrna"
    phone = "+380661234567"
    address = "Ukraine"

    class Meta:
        model = Client


class TypeFactory(factory.django.DjangoModelFactory):
    name = "Circular"

    class Meta:
        model = Type


class ColorFactory(factory.django.DjangoModelFactory):
    name = "Red"
    shade = "Burgundy"

    class Meta:
        model = Color


class WheelFactory(factory.django.DjangoModelFactory):
    name = "Wheel Test 1"

    class Meta:
        model = Wheel
