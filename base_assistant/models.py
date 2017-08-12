from django.db import models

# Create your models here.
#Sclass Version_Info(models.Model):
class VersionInfo(models.Model):
    product = models.CharField(max_length=20)
    platform_ver = models.CharField(max_length=20)
    product_ver = models.CharField(max_length=20)
    verinfo = models.CharField(max_length=200)
