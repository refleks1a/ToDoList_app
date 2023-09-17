from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Task


class CustomLogInView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class CustomRegistrationView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(CustomRegistrationView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(CustomRegistrationView, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView): #LoginRequiredMixin restrict unauthonticated user
    model = Task
    template_name = 'base/tasks.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):   #User gets only his data
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(complete = False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            print(search_input)
            context['tasks'] = context['tasks'].filter(title__icontains = search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'base/detail.html'
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    template_name = 'base/form.html'
    model = Task
    success_url = reverse_lazy('tasks')
    fields = ['title', 'description', 'complete']

    def form_valid(self, form): #Add own task
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'base/form.html'
    model = Task
    success_url = reverse_lazy('tasks')
    fields = ['title', 'description', 'complete']


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'base/delete.html'
    context_object_name = 'task'

