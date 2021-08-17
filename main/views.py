from django.shortcuts import render
from .models import Content, Comment
from django.views.generic import DetailView
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.edit import FormMixin
from .forms import LoginForm, RegisterForm, CommentForm
from django.urls import reverse


def home(request):
    content = Content.objects.order_by('-id')[:8]
    return render(request, 'main/home.html', {'content': content})


def archive(request):
    content = Content.objects.order_by('-id')
    return render(request, 'main/archive.html', {'content': content})


class NewPageSite(FormMixin, DetailView):
    model = Content
    template_name = 'main/program.html'
    context_object_name = 'content'
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse('new_page', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.key_comment = self.get_object()
        self.object.save()
        return super().form_valid(form)


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        context = {'form': form}
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'register.html', context)


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'login.html', context)
