from django.urls import path
from .views import CreateGraph, display_graph, save_graph

app_name = 'graph'

urlpatterns = [
    path('create/<str:name>', CreateGraph.as_view(), name='create_graph'),
    path('<str:name>/result', display_graph, name='display_graph'),
    path('save/', save_graph, name="save_graph")
]