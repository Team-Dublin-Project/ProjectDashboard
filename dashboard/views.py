from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.

class HomeView(LoginRequiredMixin, View):
    template_name = 'home.html'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
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