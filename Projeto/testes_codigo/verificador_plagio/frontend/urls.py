from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('result', index),
    path('homepage', index),
    path('details', index),
]
