from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('how-to-order/', views.how_to_order, name='how_to_order'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]
