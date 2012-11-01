from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from renamer.helpers.directoryinfo import list_directory, check_difference, check_intersection


# @login_required(login_url='/login/')
def home(request):
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

    return render(request, 'main/home.html', data)


# @login_required(login_url='/login/')
def to_archive(request):
    pass


# @login_required(login_url='/login/')
def to_diva(request):
    pass


# @login_required(login_url='/login/')
def diva_redo(request):
    pass
