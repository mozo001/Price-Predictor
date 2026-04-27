from django.db import models

# Create your models here.
class Prediction(models.Model):
    feature1 = models.FloatField()
    feature2 = models.FloatField()
    predicted_price = models.FloatField()