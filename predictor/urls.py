from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_laptop/', views.add_laptop, name='add_laptop'),
    path('edit_laptop/<int:laptop_id>/', views.edit_laptop, name='edit_laptop'),
    path('delete_laptop/<int:laptop_id>/', views.delete_laptop, name='delete_laptop'),
]