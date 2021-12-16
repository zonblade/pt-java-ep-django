from django.db import models

# Create your models here.
class item(models.Model):
    nama = models.CharField(null=False,max_length=255)
    
class pajak(models.Model):
    nama    = models.CharField(null=False,max_length=255)
    rate    = models.DecimalField(null=False,max_digits=11,decimal_places=2)

class tests(models.Model):
    nama = models.CharField(null=False,max_length=255)
    