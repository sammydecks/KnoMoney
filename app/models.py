from django.db import models
from django.utils import timezone

# Create your models here
class Referral(models.Model):
    referral_id = models.AutoField(primary_key=True, serialize=True)
    email = models.EmailField(max_length=255)
    submit_time = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.email


# Example model?
class MyModel(models.Model):
    name = models.CharField(max_length=255)

class TestTable(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name