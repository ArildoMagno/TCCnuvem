from django.urls import path
from .views import CalculateSimilarity, GeneratePDF

urlpatterns = [
    path('calculate-similarity', CalculateSimilarity.as_view()),
    path('generate-pdf', GeneratePDF.as_view())
]
