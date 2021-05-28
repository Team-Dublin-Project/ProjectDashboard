from django.contrib import admin
from .models import Graph

# Register your models here.

class GraphAdmin(admin.ModelAdmin):
    model = Graph
    list_display = ('title', 'description', 'image', 'created')
    list_filter = ['created', 'user']
admin.site.register(Graph, GraphAdmin)
