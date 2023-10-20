from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

SERVICE_CHOICES = (
    ("Electrician", "Electrician"),
    ("Plumber", "Plumber"),

    )
TIME_CHOICES = (
    ("3 PM", "3 PM"),
    ("3:30 PM", "3:30 PM"),
    ("4 PM", "4 PM"),
    ("4:30 PM", "4:30 PM"),
    ("5 PM", "5 PM"),
    ("5:30 PM", "5:30 PM"),
    ("6 PM", "6 PM"),
    ("6:30 PM", "6:30 PM"),
    ("7 PM", "7 PM"),
    ("7:30 PM", "7:30 PM"),
)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Electrician")
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"


from django.db import models

class Staff(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100)
    tier = models.CharField(max_length=50,default="Not assigned")
    service = models.CharField(max_length=100)
    bio = models.TextField()
    experience = models.IntegerField()
    rating = models.FloatField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return f"{self.name} | {self.tier} | {self.contact_number} | {self.rating}"
