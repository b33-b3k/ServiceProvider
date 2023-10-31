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
DAY_CHOICES=(
    #%Y-%m-%d format
    
    ("2023-11-03","2023-11-03"
     ),
    ("2023-11-04","2023-11-04"
     ),
    ("2023-11-05","2023-11-05"
     ),
    ("2023-11-06","2023-11-06"
     ),
    ("2023-11-07","2023-11-07"
     ),
    ("2023-11-08","2023-11-08"
     ),
    ("2023-11-09","2023-11-09"
     ),
  
    
)


class Appointment(models.Model):
    #declare a id
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="Electrician")
    day= models.CharField(max_length=50,choices=DAY_CHOICES, default="Monday")
    address = models.CharField(max_length=50, blank=True)
    isFinished = models.CharField(max_length=15,default="No")
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM", null=True, blank=True)
    staff = models.CharField(max_length=50, default="Not assigned")

    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"



class Staff(models.Model):
    
    name = models.CharField(max_length=100)
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='email address',
        default=""
    
    )
    contact_number = models.CharField(max_length=100)
    inquiry_message = models.TextField(default="")
    assigned_user= models.CharField(max_length=100,default="")
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False,blank=True)
    # email = models.EmailField()
    # time = models.CharField(max_length=100)
    tier = models.CharField(max_length=50,default="Not assigned")
    service = models.CharField(max_length=100)
    bio = models.TextField(default='')
    experience = models.IntegerField(default='1')
    rating = models.FloatField(default='3')
    TIER_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        # ... any other tiers ...
    ]
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default='bronze')

    # image = models.ImageField(upload_to='images/', null=True, blank=True)
    # price = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return f"{self.name} | {self.tier} | {self.contact_number} | {self.rating}"

class VendorRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    business_address = models.TextField()
    
    
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    business_description = models.TextField()
    business_category = models.CharField(max_length=255)
    pan_number = models.CharField(max_length=255)
    

    def __str__(self):
        return f"{self.user.username} | {self.business_name} | {self.business_category} | {self.pan_number}"


    

class Inquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    staff_name = models.CharField(max_length=40)
    isFinished= models.CharField(max_length=15, default="No")

    
    message = models.TextField()
    replied = models.BooleanField(default=False)
    reply_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Inquiry from {self.user.username} - {self.subject}"

    

    
