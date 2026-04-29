from django.db import models

# Create your models here.


class Laptop(models.Model):
    # 'null=True, blank=True' allows the field to be empty (triggering our imputer!)
    condition = models.FloatField(null=True, blank=True) 
    age = models.FloatField(null=True, blank=True)
    
    # We will save the prediction here after the ML model runs
    predicted_price = models.FloatField(null=True, blank=True)
    
    # Keeps track of when the prediction was made
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Laptop - Prediction: {self.predicted_price}"