import pandas as pd
import base64
import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from dashboard.models import UserFile
from .forms import GraphTypeForm, SaveGraphForm
from .graph import Graph
# Create your views here.


class CreateGraph(View):
    template_name = 'create_graph.html'

    def get(self, request, name):
        file = get_object_or_404(UserFile, name=name)
        form = GraphTypeForm(file=file)
        context = {'form': form, 'name':name}
        return render(request, self.template_name, context)

    def post(self, request, name):
        file = get_object_or_404(UserFile, name=name)
        graph = Graph(request)
        form = GraphTypeForm(request.POST, file=file)
        if form.is_valid():
            cd = form.cleaned_data
            graph.set_session(file=file,
                            type = cd['type'],
                            x_values = cd['x_values'],
                            y_values = cd['y_values']
            )
            return redirect('graph:display_graph', file.name)
        else:
            return render(request, self.template_name)

def display_graph(request, name):
    file = get_object_or_404(UserFile, name=name)
    graph = request.session.get('graph')
    df = pd.read_csv(f'media/{file.file_loc}')
    if df[graph['x_values']].isna().values.any():
        df[graph['x_values']] = df[graph['x_values']].fillna(0)
    if df[graph['y_values']].isna().values.any():
        df[graph['y_values']] = df[graph['y_values']].fillna(0)

    form = SaveGraphForm()
    context = {
        'form' : form,
        'file' : file,
        'column_names' : df.columns.values,
        'row_data' : list(df.values.tolist()),
        'type': graph['type'],
        'values' : df[graph['x_values']].to_json(),
        'labels' : df[graph['y_values']].to_json(), 
    }
    return render(request, 'graph.html', context)

@require_POST
def save_graph(request):
    data = request.POST['image-url']
    file_name, data = format_dataUrl(data)
    form = SaveGraphForm(request.POST, request.FILES)

    if form.is_valid():
        graph = form.save(commit=False)
        graph.user = request.user
        graph.title = form.cleaned_data['title']
        graph.description = form.cleaned_data['description']
        graph.image.save(file_name, data, save=True)
        graph.save()
        return redirect('home')

def format_dataUrl(data):
    format, imgstr = data.split(';base64,') 
    ext = format.split('/')[-1] 
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    letters = string.ascii_lowercase
    letters = ''.join(random.choice(letters) for i in range(10)) 
    file_name = letters + "." + ext
    return file_name, data

