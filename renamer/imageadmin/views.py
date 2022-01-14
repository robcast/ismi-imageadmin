import os
import logging
import shutil

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from imageadmin.helpers.directoryinfo import list_directory, check_difference, check_intersection, alphanum_key
from imageadmin.helpers.to_archive import move_to_archive
from imageadmin.helpers.to_diva import convert_to_diva
from imageadmin.forms import LoginForm


@login_required
def home(request):
    archive_dirs = list_directory(settings.ARCHIVE_LOCATION)
    diva_dirs = list_directory(settings.DIVA_LOCATION)

    logging.debug("scanning archive directories...")
    archive_in_progress = []
    for d in archive_dirs:
        full_path = os.path.join(settings.ARCHIVE_LOCATION, d)
        if os.path.exists(os.path.join(full_path, '.work_in_progress')):
            archive_in_progress.append(d)

    logging.debug("scanning diva directories...")
    diva_in_progress = []
    for d in diva_dirs:
        full_path = os.path.join(settings.DIVA_LOCATION, d)
        if os.path.exists(os.path.join(full_path, '.diva_conversion_in_progress')):
            diva_in_progress.append(d)

    data = {
        'archive_in_progress': archive_in_progress,
        'diva_in_progress': diva_in_progress
    }
    return render(request, 'imageadmin/home.html', data)


@login_required
def view_all_diva(request):
    diva_dirs = list_directory(settings.DIVA_LOCATION)
    diva_dirs.sort(key=alphanum_key)

    data = {
        'diva_dirs': diva_dirs
    }

    return render(request, 'imageadmin/view_all_diva.html', data)


@login_required
def view_diva(request, document_id):

    data = {
        'diva_dir': document_id,
        'manifest_url': settings.IIIF_MANIF_BASE_URL + '/' + document_id + '.json',
        'auth_token_url': settings.IIIF_TOKEN_URL,
        'auth_login_url': settings.IIIF_LOGIN_URL,
    }

    return render(request, 'imageadmin/view_diva.html', data)


@login_required
def show_to_archive(request):
    archive_dirs = list_directory(settings.ARCHIVE_LOCATION)
    incoming_dirs = list_directory(settings.INCOMING_LOCATION)

    incoming_to_archive = check_difference(incoming_dirs, archive_dirs)
    incoming_to_archive.sort(key=alphanum_key)

    data = {
        'to_archive': incoming_to_archive,
    }

    return render(request, 'imageadmin/show_to_archive.html', data)


@login_required
def show_to_diva(request):
    archive_dirs = list_directory(settings.ARCHIVE_LOCATION)
    diva_dirs = list_directory(settings.DIVA_LOCATION)

    archive_to_diva = check_difference(archive_dirs, diva_dirs)
    archive_to_diva.sort(key=alphanum_key)

    data = {
        'to_diva': archive_to_diva,
    }

    return render(request, 'imageadmin/show_to_diva.html', data)


@login_required
def show_diva_redo(request):
    archive_dirs = list_directory(settings.ARCHIVE_LOCATION)
    diva_dirs = list_directory(settings.DIVA_LOCATION)

    diva_redo = check_intersection(archive_dirs, diva_dirs)
    diva_redo.sort(key=alphanum_key)

    data = {
        'diva_redo': diva_redo
    }

    return render(request, 'imageadmin/show_diva_redo.html', data)


@login_required
def to_archive(request):
    filenames = request.POST.getlist('to_archive_chk')
    absolute_filenames = [os.path.join(settings.INCOMING_LOCATION, f) for f in filenames]
    for f in absolute_filenames:
        move_to_archive.delay(f)
        
    return redirect("home")


@login_required
def to_diva(request):
    filenames = request.POST.getlist('to_diva_chk')
    absolute_filenames = [os.path.join(settings.ARCHIVE_LOCATION, f) for f in filenames]
    for f in absolute_filenames:
        convert_to_diva.delay(f)
        
    return redirect("home")


@login_required
def diva_redo(request):
    filenames = request.POST.getlist('redo_diva_chk')
    old_filenames = [os.path.join(settings.DIVA_LOCATION, f) for f in filenames]
    archive_filenames = [os.path.join(settings.ARCHIVE_LOCATION, f) for f in filenames]
    logging.debug(f"removing old files in {old_filenames}")
    for f in old_filenames:
        shutil.rmtree(f)

    for f in archive_filenames:
        convert_to_diva.delay(f)
        
    return redirect("home")


def user_login(request):
    if request.user.is_authenticated:
        redirect('home')

    if not request.POST:
        form = LoginForm()
        data = {
            'form': form,
            'form_action': request.get_full_path()
        }
        return render(request, 'imageadmin/login.html', data)
    
    else:
        form = LoginForm(request.POST)
        if not form.is_valid():
            return redirect('home')
        else:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return redirect('home')
            else:
                return redirect('user_login')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return redirect('home')
