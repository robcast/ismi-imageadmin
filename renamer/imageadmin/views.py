import os
import logging
import shutil
import re

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from renamer.celery import app as celery_app
from django_celery_results.models import TaskResult
from imageadmin.models import Directory
from imageadmin.helpers.directory_cache import scan_directory
from imageadmin.helpers.directoryinfo import check_difference, check_intersection, alphanum_key
from imageadmin.helpers.to_archive import move_to_archive
from imageadmin.helpers.to_diva import convert_to_diva
from imageadmin.forms import LoginForm



def _scan_incoming():
    return scan_directory(settings.INCOMING_LOCATION)

def _scan_archive():
    return scan_directory(settings.ARCHIVE_LOCATION, '.work_in_progress')

def _scan_diva():
    return scan_directory(settings.DIVA_LOCATION, '.diva_conversion_in_progress')

def _list_incoming():
    _scan_incoming()
    return list(Directory.objects.get(path=settings.INCOMING_LOCATION)
                .direntry_set.all()
                .values_list('name', flat=True))

def _list_archive():
    _scan_archive()
    return list(Directory.objects.get(path=settings.ARCHIVE_LOCATION)
                .direntry_set.all()
                .values_list('name', flat=True))

def _list_diva():
    _scan_diva()
    return list(Directory.objects.get(path=settings.DIVA_LOCATION)
                .direntry_set.all()
                .values_list('name', flat=True))


@login_required
def home(request):
    """
    show lists of in-progress archive and diva directories
    """
    # check archive location
    _scan_archive()
    # list names of all in_progress direntries
    archive_in_progress = list(Directory.objects.get(path=settings.ARCHIVE_LOCATION)
                               .direntry_set.filter(in_progress=True)
                               .values_list('name', flat=True))
    # check diva location
    _scan_diva()
    # list names of all in_progress direntries
    diva_in_progress = list(Directory.objects.get(path=settings.DIVA_LOCATION)
                            .direntry_set.filter(in_progress=True)
                            .values_list('name', flat=True))
    
    # list running celery tasks
    workers = celery_app.control.inspect()
    celery_registered = [t for t in workers.registered().values() if t]
    logging.debug(f"registered tasks: {celery_registered}")
    celery_active = [t for t in workers.active().values() if t]
    logging.debug(f"active tasks: {celery_active}")
    celery_scheduled = [t for t in workers.scheduled().values() if t]
    logging.debug(f"scheduled tasks: {celery_scheduled}")
    
    # list completed task results
    celery_results = TaskResult.objects.values()
    
    data = {
        'archive_in_progress': archive_in_progress,
        'diva_in_progress': diva_in_progress,
        'celery_active': celery_active,
        'celery_results': celery_results
    }
    return render(request, 'imageadmin/home.html', data)


@login_required
def view_task_result(request, task_id):
    """
    show one celery task result
    """
    # list completed task results
    celery_result = TaskResult.objects.filter(task_id=task_id).values()
    if celery_result:
        celery_result = celery_result[0]
        logging.debug(f"celery_result: {repr(celery_result)}")
        celery_result['str_result'] = celery_result['result'].strip('"').replace('\\n', '\n')
        
    data = {
        'celery_result': celery_result
    }

    return render(request, 'imageadmin/view_task_result.html', data)



@login_required
def view_all_diva(request):
    """
    show a list of all diva directories
    """
    diva_dirs = _list_diva()
    diva_dirs.sort(key=alphanum_key)

    data = {
        'diva_dirs': diva_dirs
    }

    return render(request, 'imageadmin/view_all_diva.html', data)


def view_diva(request, document_id):
    """
    show one diva directory using Diva.js
    """
    data = {
        'diva_dir': document_id,
        'manifest_url': settings.IIIF_MANIF_BASE_URL + '/' + document_id + '.json',
        'auth_token_url': settings.IIIF_TOKEN_URL,
        'auth_login_url': settings.IIIF_LOGIN_URL,
    }

    return render(request, 'imageadmin/view_diva.html', data)


def view_ext_diva(request, manifest_url=None):
    """
    show external iiif manifest using Diva.js
    """
    if manifest_url is None:
        manifest_url = request.GET.get('url')
        
    # fix munged protocol part
    proto_match = re.match(r'(https?)://?(.+)', manifest_url)
    if proto_match:
        manifest_url = proto_match.group(1) + '://' + proto_match.group(2)
    else:
        manifest_url = 'https://' + manifest_url
        
    data = {
        'manifest_url': manifest_url
    }

    return render(request, 'imageadmin/view_ext_diva.html', data)


@login_required
def show_to_archive(request):
    """
    show a select list of all incoming directories that are not in archive
    """
    archive_dirs = _list_archive()
    incoming_dirs = _list_incoming()

    incoming_to_archive = check_difference(incoming_dirs, archive_dirs)
    incoming_to_archive.sort(key=alphanum_key)

    data = {
        'to_archive': incoming_to_archive,
    }

    return render(request, 'imageadmin/show_to_archive.html', data)


@login_required
def show_to_diva(request):
    """
    show a select list of all archive directories that are not in diva
    """
    archive_dirs = _list_archive()
    diva_dirs = _list_diva()

    archive_to_diva = check_difference(archive_dirs, diva_dirs)
    archive_to_diva.sort(key=alphanum_key)

    data = {
        'to_diva': archive_to_diva,
    }

    return render(request, 'imageadmin/show_to_diva.html', data)


@login_required
def show_diva_redo(request):
    """
    show a select list of all archive directories that are in diva
    """
    archive_dirs = _list_archive()
    diva_dirs = _list_diva()

    diva_redo = check_intersection(archive_dirs, diva_dirs)
    diva_redo.sort(key=alphanum_key)

    data = {
        'diva_redo': diva_redo
    }

    return render(request, 'imageadmin/show_diva_redo.html', data)


@login_required
def to_archive(request):
    """
    start archive jobs for submitted directories
    """
    filenames = request.POST.getlist('to_archive_chk')
    absolute_filenames = [os.path.join(settings.INCOMING_LOCATION, f) for f in filenames]
    for f in absolute_filenames:
        move_to_archive.delay(f)
        
    return redirect("home")


@login_required
def to_diva(request):
    """
    start diva conversion jobs for submitted directories
    """
    filenames = request.POST.getlist('to_diva_chk')
    absolute_filenames = [os.path.join(settings.ARCHIVE_LOCATION, f) for f in filenames]
    for f in absolute_filenames:
        convert_to_diva.delay(f)
        
    return redirect("home")


@login_required
def diva_redo(request):
    """
    start diva re-generation jobs for submitted directories
    """
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
                return redirect('login')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return redirect('home')
