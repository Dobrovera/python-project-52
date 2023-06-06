from django.contrib import messages
from django.utils.translation import gettext
from .models import Task
from django.shortcuts import render, redirect
from django.views import View
from .forms import TaskCreateForm

class TasksListView(View):

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        return render(request, 'tasks/tasks.html', context={
            "tasks": tasks,
        })


class TaskCreateView(View):

    def get(self, request, *args, **kwargs):
        form = TaskCreateForm()
        return render(request, 'tasks/task_create.html', context={
            "form": form
        })

    def post(self, request, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            if form['name'].value() not in Task.objects.values_list('name', flat=True).distinct():
                task = form.save(commit=False)
                task.author = request.user
                task.save()
                messages.success(request, gettext('Task created successfully'))
                return redirect('/tasks')
            else:
                text = gettext('A task with this name already exists')
                return render(request, 'tasks/task_create.html', context={'form': form, 'text': text})
        else:
            form = TaskCreateForm()
        return render(request, 'tasks/task_create.html', context={'form': form})
