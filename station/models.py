from django.db import models

class Type(models.Model):
	name = models.CharField(max_length=200)

class Spare(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    types = models.ManyToManyField(Type)

class Color(models.Model):
    name = models.CharField(max_length=20)
    shade = models.CharField(max_length=20)

class Transport(models.Model):
    title = models.CharField(max_length=200)
    spares = models.ManyToManyField(Spare)
    color = models.OneToOneField(Color, on_delete=models.CASCADE)

class Client(models.Model):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    
class Wheel(models.Model):
	name = models.CharField(max_length=200)
	transports = models.ManyToManyField(Transport)
