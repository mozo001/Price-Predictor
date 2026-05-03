from django.db import models

# Create your models here.

# predictor/models.py
from django.db import models

class Laptop(models.Model):
    company = models.CharField(max_length=200)
    type_name = models.CharField(max_length=200)
    ram = models.IntegerField()
    weight = models.FloatField()
    cpu_brand = models.CharField(max_length=200)
    gpu_brand = models.CharField(max_length=200)
    os = models.CharField(max_length=200)
    predicted_price = models.IntegerField()

    def __str__(self):
        return f"{self.company} - {self.predicted_price}"