from django.shortcuts import render
from .models import Laptop
from django.shortcuts import render, redirect
from .models import Laptop

import joblib
import numpy as np
import os
from django.conf import settings


# Create your views here.
def index(request):
    laptops = Laptop.objects.all()
 
    return render(request, 'predictor/index.html', {'laptops': laptops})



# Load once when the server starts
model_path = os.path.join(settings.BASE_DIR, 'predictor', 'laptop_model.pkl')
scaler_path = os.path.join(settings.BASE_DIR, 'predictor', 'scaler.pkl')
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

def add_laptop(request):
    if request.method == 'POST':
        # 1. Get user input
        cond = float(request.POST.get('condition'))
        age = float(request.POST.get('age'))

        # 2. Recreate the 3rd feature (Depreciation Rate)
        # Using a dummy 'original_price' of 5000 and 'current_estimate' of 2000
        # to match the logic from your notebook
        dep_rate = (5000 - 2000) / age if age > 0 else 0 

        # 3. Create the input array with 3 columns
        # The order must be exactly [condition, age, depreciation_rate]
        features = np.array([[cond, age, dep_rate]])

        # 4. Scale and Predict
        # This will now work because features has 3 columns, matching your scaler
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        
        # 5. Save to Database
        Laptop.objects.create(
            condition=cond,
            age=age,
            predicted_price = round(float(prediction[0]), 2)
        )
        return redirect('index')

def edit_laptop(request, laptop_id):
    from django.shortcuts import get_object_or_404
    laptop = get_object_or_404(Laptop, id=laptop_id)
    
    if request.method == 'POST':
        # Update the specific instance
        laptop.condition = request.POST.get('condition')
        laptop.age = request.POST.get('age')
        laptop.save() # Crucial: Save the changes
        return redirect('index')
        
    return render(request, 'predictor/edit_laptop.html', {'laptop': laptop})

def delete_laptop(request, laptop_id):
    # Use get_object_or_404 for better error handling
    from django.shortcuts import get_object_or_404
    laptop = get_object_or_404(Laptop, id=laptop_id)
    
    if request.method == 'POST':
        laptop.delete()
        return redirect('index') # Return to main page
    
    # If they just visit the URL (GET), show a confirmation page
    return render(request, 'predictor/delete_laptop.html', {'laptop': laptop})