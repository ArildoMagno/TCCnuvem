from django.urls import path
from .views import MainView, SendFilesView

urlpatterns = [
    path('main', MainView.as_view()),
    path('send-files', SendFilesView.as_view()),
]
