from django.urls import path
from .views import hello, transcribe_audio

urlpatterns = [
    path('hello/', hello),
    path('transcribe-audio/', transcribe_audio),
]
