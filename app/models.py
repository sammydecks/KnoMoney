from django.db import models

# Create your models here
class Referral(models.Model):
    referral_email = models.EmailField(max_length=254)

    def __str__(self):
        return self.referral_email


# Example model?
class MyModel(models.Model):
    name = models.CharField(max_length=255)