from django.urls import path
from .views import CalculateSimilarity, GeneratePDF, CleanFiles

urlpatterns = [
    path('calculate-similarity', CalculateSimilarity.as_view()),
    path('generate-pdf', GeneratePDF.as_view()),
    path('clean-files', CleanFiles.as_view())
]
