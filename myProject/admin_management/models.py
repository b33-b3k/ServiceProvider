# D:\ServiceProvider\myProject\admin_management\models.py

from django.db import models

class ServiceProvider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    qualifications = models.TextField()

    def __str__(self):
        return self.name


class Tier(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    benefits = models.TextField()

    def __str__(self):
        return self.name
