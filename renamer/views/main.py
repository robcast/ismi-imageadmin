from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from renamer.helpers.directoryinfo import list_directory, check_difference, check_intersection
from renamer.helpers.to_archive import move_to_archive
from renamer.helpers.to_diva import convert_to_diva
from renamer.forms.login import LoginForm
import shutil
import os


@login_required(login_url="/login/")
def home(request):
    archive_dirs = list_directory(settings.ARCHIVE_LOCATION)
    diva_dirs = list_directory(settings.DIVA_LOCATION)

    archive_in_progress = []
    for d in archive_dirs:
        full_path = os.path.join(settings.ARCHIVE_LOCATION, d)
        if os.path.exists(os.path.join(full_path, ".work_in_progress")):
            archive_in_progress.append(d)

    diva_in_progress = []
    for d in diva_dirs:
        full_path = os.path.join(settings.DIVA_LOCATION, d)
        if os.path.exists(os.path.join(full_path, ".diva_conversion_in_progress")):
            diva_in_progress.append(d)

    data = {
        "archive_in_progress": archive_in_progress,
        "diva_in_progress": diva_in_progress
    }
    return render(request, "main/home.html", data)


@login_required(login_url='/login/')
def manage(request):
    archive_dirs = list_directory(settings.ARCHIVE_LOCATION)
    incoming_dirs = list_directory(settings.INCOMING_LOCATION)
    diva_dirs = list_directory(settings.DIVA_LOCATION)

    incoming_to_archive = check_difference(incoming_dirs, archive_dirs)
    archive_to_diva = check_difference(archive_dirs, diva_dirs)
    diva_redo = check_intersection(archive_dirs, diva_dirs)

    data = {
        'to_archive': incoming_to_archive,
        'to_diva': archive_to_diva,
        'diva_redo': diva_redo
    }

    return render(request, 'main/manage.html', data)


@login_required(login_url='/login/')
def to_archive(request):
    filenames = request.POST.getlist('to_archive_chk')
    absolute_filenames = [os.path.join(settings.INCOMING_LOCATION, f) for f in filenames]
    for f in absolute_filenames:
        move_to_archive.delay(f)
    return redirect("home")


@login_required(login_url='/login/')
def to_diva(request):
    filenames = request.POST.getlist('to_diva_chk')
    absolute_filenames = [os.path.join(settings.ARCHIVE_LOCATION, f) for f in filenames]
    for f in absolute_filenames:
        convert_to_diva.delay(f)
    return redirect("home")


@login_required(login_url='/login/')
def diva_redo(request):
    filenames = request.POST.getlist('redo_diva_chk')
    old_filenames = [os.path.join(settings.DIVA_LOCATION, f) for f in filenames]
    archive_filenames = [os.path.join(settings.ARCHIVE_LOCATION, f) for f in filenames]
    for f in old_filenames:
        shutil.rmtree(f)

    for f in archive_filenames:
        convert_to_diva.delay(f)
    return redirect("home")


def user_login(request):
    if request.user.is_authenticated():
        redirect("home")

    if not request.POST:
        form = LoginForm()
        data = {
            'form': form,
            'form_action': request.get_full_path()
        }
        return render(request, 'main/login.html', data)
    else:
        form = LoginForm(request.POST)
        if not form.is_valid():
            return redirect("home")
        else:
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("home")
                else:
                    return redirect("home")
            else:
                return redirect("user_login")


def user_logout(request, *args, **kwargs):
    if request.user.is_authenticated():
        logout(request)
        return redirect("home")
    else:
        return redirect("home")
