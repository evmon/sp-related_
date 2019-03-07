import factory
from .models import Spare, Transport, Client, Type, Color, Wheel

class SpareFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Spare

    country = "USA"
    name = "Head Lights"


class TransportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transport


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    name = "Evheniya Monastyrna"
    phone = "+380661234567"
    address = "Ukraine"


class TypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Type

    name = "Circular"


class ColorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Color

    name = "Red"
    shade = "Burgundy"


class WheelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wheel

    name = "Wheel Test 1"
