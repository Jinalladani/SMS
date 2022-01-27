from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class OtpModel(models.Model):
    mobile_number = PhoneNumberField()
    otp = models.CharField(max_length=6)