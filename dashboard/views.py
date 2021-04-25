import csv, io
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import FileForm
from .models import UserFile
from django.contrib import messages
from IPython.display import display

# Create your views here.

class HomeView(LoginRequiredMixin, View):
    template_name = 'home.html'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        files = None
        out = None
        headers = None
        csv_f = None
        df_list = []
        username = request.user
        file_form = FileForm()
        if UserFile.objects.filter(user=username).exists():
            files = UserFile.objects.filter(user=username)
            for f in files:
                temp_df = pd.read_csv(f'media/{f.file_name}')
                df_list.append(temp_df)
                #reader = csv.DictReader(csv_fp)
                #headers = [col for col in reader.fieldnames]
                #out = [row for row in reader]
            for dataset in df_list:
                display(dataset)
        context = {'file_form': file_form, 'files': files, 'df_list': df_list, 'csv_f': csv_f}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            file_form = FileForm(request.POST, request.FILES) 
            ufile = request.FILES['file']
            if not ufile.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
                return redirect('home')
            else:
                '''
                data_set = ufile.read().decode('utf-8-sig')
                io_string = io.StringIO(data_set)
                spamreader = csv.reader(io_string, delimiter=',')
                for row in spamreader:
                   print(row)
                '''
                isheader = csv.Sniffer().has_header(ufile.read().decode('utf-8-sig'))
                if isheader and file_form.is_valid():
                    file = file_form.save(commit=False)
                    file_instance = UserFile.objects.create(user=request.user, file_name=ufile)
                    file_instance.save()
        return redirect('home')
        args = {'file_form':file_form, 'messages': messages}
        return render(request, self.template_name, args)

    '''
    def get_object(self, *args, **kwargs):
        return get_object_or_404(
        Post,
        pk=self.kwargs.get('id')
    )

    def get_queryset(self):
        qs = super(HomeView, self).get_queryset()
        return qs.filter(owner=self.request.user)

    if not ufile.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
    '''