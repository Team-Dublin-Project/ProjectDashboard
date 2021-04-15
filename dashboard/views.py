from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import FileForm
from .models import UserFile

# Create your views here.

class HomeView(LoginRequiredMixin, View):
    template_name = 'home.html'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        files = None
        username = request.user
        file_form = FileForm()
        if UserFile.objects.filter(user=username).exists():
            files = UserFile.objects.filter(user=request.user)
        context = {'file_form': file_form, 'files': files}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            file_form = FileForm(request.POST, request.FILES)
            files = request.FILES.getlist('files')
            if file_form.is_valid():
                user = request.user
                file = file_form.save(commit=False)
                print(files)
                for f in files:
                    c_type = f.content_type.split("/")
                    file_instance = UserFile.objects.create(files=f, user=user, content_type=c_type[0])
                    file_instance.save()
        return redirect('home')
        args = {'file_form':file_form}
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
    '''