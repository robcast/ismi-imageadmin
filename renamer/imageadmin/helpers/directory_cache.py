import os
import datetime
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, DatabaseError
from django.conf import settings
from imageadmin.models import Directory, DirEntry
from imageadmin.helpers.directoryinfo import list_directory

def scan_directory(path, wip_file=None):
    """
    Scan filesystem directory at path and update directory model in db.
    
    Sets in_progress in DirEnt if wip_file exists.
    
    Does not re-scan filesystem if time since last access is less than DIR_CACHE_TIMEOUT.
    """
    try:
        directory = Directory.objects.get(path=path)
        if datetime.datetime.now(tz=datetime.timezone.utc) - directory.last_access_date < settings.DIR_CACHE_TIMEOUT:
            # not ready to re-scan
            logging.debug(f"directory {path} in cache still valid")
            return

    except ObjectDoesNotExist:
        directory = Directory(path=path)
        directory.save()
        
    # run scanning the directory with database lock on directory to make sure only one scan runs at a time
    with transaction.atomic():
        try:
            directory = Directory.objects.select_for_update(nowait=True).get(path=path)
            logging.debug(f"scanning directory {path}")
            # clear dirents
            directory.direntry_set.all().delete()
            # read filesystem directory
            for d in list_directory(path):
                full_path = os.path.join(path, d)
                if wip_file:
                    in_progress = os.path.exists(os.path.join(full_path, wip_file))
                else:
                    in_progress = False
        
                # create direntry linked to directory
                directory.direntry_set.create(name=d, in_progress=in_progress)
            
            # update access time
            directory.save()
        
        except DatabaseError:
            logging.debug(f"directory {path} locked - aborting scan")
            