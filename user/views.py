from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import CreateView, View
from django.urls import reverse_lazy, reverse
from django.contrib import messages

# Create your views here.

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)

class SignInView(View):
    form = SignInForm
    template_name = 'signin.html'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        form = SignInForm()
        context = {
            'form' : form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user_obj')
            login(request, user)
            return redirect(reverse('home'))
        context = {
            'form' : form
        }
        return render(request, self.template_name, context)

class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('signin'))