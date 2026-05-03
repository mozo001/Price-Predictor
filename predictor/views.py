from django.shortcuts import render, redirect, get_object_or_404
from .models import Laptop
import joblib
import pandas as pd
import numpy as np
import os
from django.conf import settings

# Load your model pipeline
# Ensure 'laptop_model_pipe.pkl' is in your predictor folder
model_path = os.path.join(settings.BASE_DIR, 'predictor', 'laptop_model_pipe.pkl')
pipe = joblib.load(model_path)

def index(request):
    # Fetch all saved laptops to display in the grid
    laptops = Laptop.objects.all().order_by('-id')[:10]
    return render(request, 'predictor/index.html', {'laptops': laptops})

def add_laptop(request):
    if request.method == 'POST':
        # 1. Capture Form Data
        company = request.POST.get('company')
        type_name = request.POST.get('type_name')
        ram = int(request.POST.get('ram'))
        weight = float(request.POST.get('weight'))
        touchscreen = int(request.POST.get('touchscreen'))
        ips = int(request.POST.get('ips'))
        cpu = request.POST.get('cpu_brand')
        gpu = request.POST.get('gpu_brand')
        os_val = request.POST.get('os')
        inches = float(request.POST.get('screen_size'))
        
        # 2. Storage Mapping Logic (Handles Flash Storage too!)
        storage_type = request.POST.get('storage_type') 
        storage_size = int(request.POST.get('storage_size', 0))
        ssd, hdd, flash = 0, 0, 0

        if storage_type == 'SSD': ssd = storage_size
        elif storage_type == 'HDD': hdd = storage_size
        elif storage_type == 'Flash Storage': flash = storage_size
        elif storage_type == 'Hybrid':
            ssd, hdd = 256, 1000 # Standard hybrid assumption

        # 3. PPI Calculation
        res = request.POST.get('resolution')
        X_res, Y_res = int(res.split('x')[0]), int(res.split('x')[1])
        ppi = ((X_res**2) + (Y_res**2))**0.5 / inches

        # 4. DataFrame (Must match X order in Notebook)
        query = pd.DataFrame([[
            company, type_name, ram, weight, touchscreen, ips, ppi, 
            cpu, gpu, os_val, inches, hdd, ssd, flash
        ]], columns=['Company', 'TypeName', 'Ram', 'Weight', 'Touchscreen', 'Ips', 'ppi', 'Cpu_brand', 'Gpu_brand', 'OpSys', 'Inches', 'HDD', 'SSD', 'Flash'])

        # 5. Predict & Save
        prediction = pipe.predict(query)[0]
        final_price = int(np.exp(prediction))

        Laptop.objects.create(
            company=company, type_name=type_name, ram=ram, weight=weight,
            cpu_brand=cpu, gpu_brand=gpu, os=os_val, predicted_price=final_price
        )
        return redirect('index')

def delete_laptop(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    laptop.delete()
    return redirect('index')

def edit_laptop(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    
    if request.method == 'POST':
        # 1. Update Basic Fields
        laptop.company = request.POST.get('company')
        laptop.type_name = request.POST.get('type_name')
        laptop.ram = int(request.POST.get('ram'))
        laptop.weight = float(request.POST.get('weight'))
        laptop.cpu_brand = request.POST.get('cpu_brand')
        laptop.gpu_brand = request.POST.get('gpu_brand')
        laptop.os = request.POST.get('os')
        
        # 2. Get the new specs for the prediction
        inches = float(request.POST.get('screen_size', 15.6)) # Use 15.6 as default
        res = request.POST.get('resolution', '1920x1080')
        X_res, Y_res = int(res.split('x')[0]), int(res.split('x')[1])
        ppi = ((X_res**2) + (Y_res**2))**0.5 / inches

        # Storage Logic (Crucial for the missing columns!)
        st_type = request.POST.get('storage_type', 'SSD')
        st_size = int(request.POST.get('storage_size', 256))
        ssd, hdd, flash = 0, 0, 0
        if st_type == 'SSD': ssd = st_size
        elif st_type == 'HDD': hdd = st_size
        elif st_type == 'Flash Storage': flash = st_size

        # 3. Build the COMPLETE DataFrame (Order is critical)
        query = pd.DataFrame([[
            laptop.company, laptop.type_name, laptop.ram, laptop.weight,
            int(request.POST.get('touchscreen', 0)), int(request.POST.get('ips', 0)),
            ppi, laptop.cpu_brand, laptop.gpu_brand, laptop.os,
            inches, hdd, ssd, flash
        ]], columns=['Company', 'TypeName', 'Ram', 'Weight', 'Touchscreen', 'Ips', 'ppi', 'Cpu_brand', 'Gpu_brand', 'OpSys', 'Inches', 'HDD', 'SSD', 'Flash'])

        # 4. Predict and Save
        prediction = pipe.predict(query)[0]
        laptop.predicted_price = int(np.exp(prediction))
        laptop.save()
        return redirect('index')

    return render(request, 'predictor/edit_laptop.html', {'laptop': laptop})