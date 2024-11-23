from django.db import models

# Create your models here.
class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    cellphone = models.CharField(max_length=12)
    description = models.TextField(max_length=500)

class Pages(models.Model):
    namePage = models.CharField(max_length=20)
    click = models.BooleanField()