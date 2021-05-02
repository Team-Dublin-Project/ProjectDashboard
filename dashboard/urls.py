from django.urls import path
from .views import HomeView, TableDeleteView
from dashboard import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('tables/<str:username>', views.display_tables, name='display_tables'),
    path('tables/<pk>/delete/', TableDeleteView.as_view(), name='delete_table'),
]