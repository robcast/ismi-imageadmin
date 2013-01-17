from celery import task
from celery import current_task
from celery import states
import os
import shutil
import re
import sys
import hashlib
import zipfile
import subprocess
from django.conf import settings
from renamer.helpers.directoryinfo import alphanum_key

valid_extensions = [".pdf", ".zip", ".jpg", ".jpeg", ".tif", ".tiff", ".JPG", ".JPEG", ".TIF", ".TIFF", ".PDF", '.png', '.PNG']
RE_uuid = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
RE_spaces = r"[\s]+"
RE_underscores = r"[_]+"


@task(ignore_result=True)
def move_to_archive(incoming_directory):
    incoming_directory = incoming_directory.rstrip("/")
    archive_directory = settings.ARCHIVE_LOCATION
    if not os.path.exists(os.path.join(incoming_directory, "pageimg")):
        f = open(os.path.join(incoming_directory, '.rename_failed'), 'w')
        f.close()
        current_task.update_state(state=states.FAILURE)
        return False

    basedir = os.path.split(incoming_directory)
    new_msdir = __clean_dirname(basedir[-1])
    full_ms_path = os.path.join(archive_directory, new_msdir)
    shutil.move(incoming_directory, full_ms_path)

    f = open(os.path.join(full_ms_path, '.work_in_progress'), 'w')
    f.close()

    full_pgimg_path = os.path.join(full_ms_path, "pageimg")
    full_info_path = os.path.join(full_ms_path, "info")
    full_backup_path = os.path.join(full_ms_path, "backup")

    fnames = os.listdir(full_pgimg_path)
    fnames.sort(key=alphanum_key)
    all_extensions = set([os.path.splitext(f)[-1].lower() for f in fnames])

    if ".zip" in all_extensions:
        if not os.path.exists(full_backup_path):
            os.mkdir(full_backup_path)

        for f in fnames:
            if os.path.splitext(f)[-1] != ".zip":
                continue
            infname = os.path.join(full_pgimg_path, f)
            try:
                zipf = zipfile.ZipFile(infname)
                for name in zipf.namelist():
                    z = open(os.path.join(full_pgimg_path, name), 'wb')
                    z.write(zipf.read(name))
                    z.close()
                zipf.close()
            except:
                # zipfile open failed. Pass along a message and fail the task.
                current_task.update_state(state=states.FAILURE)
                return False

        os.rename(infname, os.path.join(full_backup_path, f))

    fnames = [f for f in os.listdir(full_pgimg_path) if __filter_fnames(f)]
    fnames.sort(key=alphanum_key)

    all_extensions = set([os.path.splitext(f)[-1].lower() for f in fnames])
    if ".pdf" in all_extensions:
        # process pdf files
        try:
            fnames = __process_pdfs(fnames, full_pgimg_path, full_backup_path)
        except:
            # pdf convert failed. Pass along a message and fail the task.
            current_task.update_state(state=states.FAILURE)
            return False

    for num, fn in enumerate(fnames):
        ext = os.path.splitext(fn)[-1].lower()
        new_fn = "{0}_{1}{2}".format(new_msdir, str(num).zfill(4), ext)
        os.rename(os.path.join(full_pgimg_path, fn), os.path.join(full_pgimg_path, new_fn))

    if not os.path.exists(full_info_path):
        os.mkdir(full_info_path)

    info_file = os.path.join(full_info_path, "CHECKSUMS.sha1")
    sh = open(info_file, 'w')
    imgs = os.listdir(full_pgimg_path)
    imgs.sort(key=alphanum_key)
    pimg = [f for f in imgs if __filter_fnames(f)]
    for f in pimg:
        csum = __csum_file(os.path.join(full_pgimg_path, f))
        fname = os.path.relpath(os.path.join(full_pgimg_path, f), full_ms_path)
        sh.write("{0} {1}\n".format(csum, fname))

    if os.path.exists(full_backup_path):
        bimgs = os.listdir(full_backup_path)
        bimgs.sort(key=alphanum_key)
        bkup = [f for f in bimgs if __filter_fnames(f)]
        for f in bkup:
            csum = __csum_file(os.path.join(full_backup_path, f))
            fname = os.path.relpath(os.path.join(full_backup_path, f), full_ms_path)
            sh.write("{0} {1}\n".format(csum, fname))
    sh.close()

    os.remove(os.path.join(full_ms_path, '.work_in_progress'))

    f = open(os.path.join(full_ms_path, '.rename_done'), 'w')
    f.close()
    return True


def __filter_fnames(fname):
    if fname.startswith('.'):
        return False
    if fname == "Thumbs.db":
        return False
    if os.path.splitext(fname)[-1].lower() not in valid_extensions:
        return False
    return True


def __csum_file(filename):
    retcode = None
    try:
        retcode = subprocess.Popen([settings.PATH_TO_SHASUM,
                            filename], stdout=subprocess.PIPE)
    except:
        sys.stdout.write("\trna ERROR: >>>>>> COULD NOT CHECKSUM FILE {0}\n".format(filename))
        sys.stdout.flush()
        raise(Exception)  # gettin' outta dodge

    output = retcode.communicate()
    res = output[0].read().strip().split("  ")
    return res[0]


def __clean_dirname(msdir):
    # remove any extraneous spaces
    newdir = re.sub(RE_spaces, "_", msdir)
    # ensure we only ever have one underscore (in case there was " _")
    newdir = re.sub(RE_underscores, "_", newdir)
    return newdir


def __process_pdfs(fnames, pgimg_path, backup_path):
    for f in fnames:
        if os.path.splitext(f)[-1] != ".pdf":
            continue

        fname_pattern = "{0}-%04d.png".format(os.path.splitext(f)[0])
        infname = os.path.join(pgimg_path, f)
        outfname = os.path.join(pgimg_path, fname_pattern)
        try:
            _ = subprocess.call([settings.PATH_TO_GS,
                                        "-dNOPAUSE",
                                        "-q",
                                        "-r150x150",
                                        "-sDEVICE=png16m",
                                        "-dBATCH",
                                        "-o", outfname,
                                        infname], env={"TEMP": settings.TMPDIR})
        except:
            raise(Exception)  # gettin' outta dodge

        # make a backup copy of the original PDF file
        if not os.path.exists(backup_path):
            os.mkdir(backup_path)
        os.rename(infname, os.path.join(backup_path, f))

    retval = [f for f in os.listdir(pgimg_path) if __filter_fnames(f)]
    retval.sort(key=alphanum_key)
    return retval
