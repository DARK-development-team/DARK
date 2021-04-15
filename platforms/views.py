from django.shortcuts import render, redirect
from platforms.forms import PlatformForm
from platforms.models import Platform
import os
from . import platform_utils


def add_platform_view(request):
    if request.method == 'POST':
        form = PlatformForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')

            platform = Platform(name=name, address=address)
            platform.save()

            platform_utils.clone_repo(name, address)

            return redirect('platforms:Platform Details', platform.pk)

    else:
        form = PlatformForm()

    return render(request, 'platforms/platform_form.html', {'form': form})


def platform_details_view(request, platform_id):
    platform = Platform.objects.get(pk=platform_id)
    return render(request, 'platforms/platform_details.html', {'platform': platform})

