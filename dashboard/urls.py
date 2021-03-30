from django.urls import path
from .views import HomeView
from dashboard import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]