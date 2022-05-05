from django.urls import path
from .views import CalculateSimilarity

urlpatterns = [
    path('calculate-similarity', CalculateSimilarity.as_view()),
]
