from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_laptop/', views.add_laptop, name='add_laptop'),
    path('edit_laptop/<int:pk>/', views.edit_laptop, name='edit_laptop'),
    # In your urls.py
    path('delete_laptop/<int:pk>/', views.delete_laptop, name='delete_laptop'),
]