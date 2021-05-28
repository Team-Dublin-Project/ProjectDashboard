from .graph import Graph

def graph(request):
    return {'graph': Graph(request)}