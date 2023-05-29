from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Statuses
from task_manager.views import index
from .forms import StatusesForm, UpdateStatusForm
from django.utils.translation import gettext


class StatusesList(View):

    def get(self, request, *args, **kwargs):
        statuses = Statuses.objects.all()
        return render(request, 'statuses/statuses.html', context={
            "statuses": statuses,
        })


class CreateStatus(View):

    def get(self, request, *args, **kwargs):
        form = StatusesForm()
        return render(request, 'statuses/statuses_create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = StatusesForm(request.POST)
        if form.is_valid():
            if form['status_name'].value() not in Statuses.objects.values_list('status_name', flat=True).distinct():
                form.save()
                messages.success(request, gettext('Status created successfully'))
                return redirect('/statuses')
            else:
                text = gettext('A task status with this name already exists')
                return render(request, 'statuses/statuses_create.html', context={'form': form, 'text': text})
        else:
            form = StatusesForm()
        return render(request, 'statuses/statuses_create.html', context={'form': form})


class DeleteStatus(View):
    def get(self, request, *args, **kwargs):
        status = get_object_or_404(Statuses, id=kwargs['id'])
        return render(request, 'statuses/status_delete.html', context={
            "status": status
        })
    def post(self, request, *args, **kwargs):
        status = get_object_or_404(Statuses, id=kwargs['id'])
        status.delete()
        messages.success(request, gettext('Status deleted successfully'))
        return redirect('/statuses')


class UpdateStatus(View):
    def get(self, request, *args, **kwargs):
        status = get_object_or_404(Statuses, id=kwargs['id'])
        status_name = status.status_name
        form = UpdateStatusForm(status.id, {"status_name": status_name})
        return render(request, 'statuses/status_update.html', context={
            "status": status,
            "form": form,
        })
    def post(self, request, *args, **kwargs):
        status = get_object_or_404(Statuses, id=kwargs['id'])
        form = UpdateStatusForm(status.id, request.POST)
        if request.POST['status_name'] not in Statuses.objects.all().values_list('status_name', flat=True):
            if form.is_valid():
                form.save()
                messages.success(request, gettext('Status updated successfully'))
                return redirect('/statuses')
        else:
            return render(request, 'statuses/status_update.html', context={
                "form": form,
            })