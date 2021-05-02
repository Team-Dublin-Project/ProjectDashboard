import csv, io, json
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DeleteView
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
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
        file_form = FileForm()
        context = {'file_form': file_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            file_form = FileForm(request.POST, request.FILES) 
            ufile = request.FILES['file']
            if not ufile.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')
                return redirect('home')
            else:
                isheader = csv.Sniffer().has_header(ufile.read().decode('utf-8-sig'))
                if isheader and file_form.is_valid():
                    file = file_form.save(commit=False)
                    file_instance = UserFile.objects.create(user=request.user, file_loc=ufile, name=ufile.name)
                    file_instance.save()
        return redirect('display_tables', username=request.user.username)
        context = {'file_form':file_form, 'messages': messages}
        return render(request, self.template_name, context)

def display_tables(request, username):
    files = None
    context = {}
    df_list = []
    if UserFile.objects.filter(user=request.user).exists():
        print(UserFile.objects.filter(id=45))
        files = UserFile.objects.filter(user=request.user)
        for f in files:
            temp_df = pd.read_csv(f'media/{f.file_loc}')
            df_list.append(temp_df)
        csv_list = zip(files, df_list)
        context = {'files': files, 'df_list': df_list, 
                    'csv_list': csv_list, 'columns': temp_df.columns
                }
    return render(request, 'tables/tables.html', context)

def has_permission(request):
    user = request.user
    return user.has_perm('dashboard.delete_userfile')

class OwnerMixin(object):
    print("hello1")

    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        print(qs)
        return qs.filter(user_id=self.request.user)

class OwnerEditMixin(object):
    def from_valid(self, form):
        form.instance.user = (self.request.user) 
        print(form.instance.user)
        return super(OwnerEditMixin, self).form_valid(form)

class OwnerTableMixin(OwnerMixin, LoginRequiredMixin):
    model = UserFile
    fields = ['file_loc']
    success_url = reverse_lazy('home')

class OwnerTableEditMixin(OwnerTableMixin, OwnerEditMixin):
    model = UserFile
    fields = ['file_loc']
    success_url = reverse_lazy('home')

class TableDeleteView(PermissionRequiredMixin, OwnerTableMixin, DeleteView):
    template_name = 'tables/delete_table.html'
    success_url = reverse_lazy('home')
    permission_required = 'dashboard.delete_userfile'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context