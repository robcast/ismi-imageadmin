from celery import task
import os
import re
import sys
import hashlib
import zipfile
import subprocess
from django.conf import settings
from renamer.helpers.to_archive import alphanum_key

valid_extensions = [".pdf", ".zip", ".jpg", ".jpeg", ".tif", ".tiff", ".JPG", ".JPEG", ".TIF", ".TIFF", ".PDF", '.png', '.PNG']
RE_uuid = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
RE_spaces = r"[\s]+"
RE_underscores = r"[_]+"


@task
def move_to_archive(incoming_directory):
    archive_directory = settings.ARCHIVE_LOCATION
    if not os.path.exists(os.path.join(incoming_directory, "pageimg")):
        f = open(os.path.join(incoming_directory, '.rename_failed'), 'w')
        f.close()
        return False

    basedir = os.path.split(incoming_directory)
    new_msdir = __clean_dirname(basedir[-1])
    full_ms_path = os.path.join(archive_directory, new_msdir)

    os.rename(incoming_directory, full_ms_path)

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
                pass

        os.rename(infname, os.path.join(full_backup_path, f))
    fnames = [f for f in os.listdir(full_pgimg_path) if __filter_fnames(f)]
    fnames.sort(key=alphanum_key)

    if ".pdf" in all_extensions:
        # process pdf files
        try:
            fnames = __process_pdfs(fnames, full_pgimg_path, full_backup_path)
        except:
            # pdf convert failed. Pass along a message and fail the task.
            pass

    for num, fn in enumerate(fnames):
        ext = os.path.splitext(fn)[-1].lower()
        new_fn = "{0}_{1}{2}".format(new_msdir, str(num).zfill(4), ext)
        os.rename(os.path.join(full_pgimg_path, fn), os.path.join(full_pgimg_path, new_fn))

    if not os.path.exists(full_info_path):
        os.mkdir(full_info_path)

    info_file = os.path.join(full_info_path, "CHECKSUMS.sha1")
    sh = open(info_file, 'w')
    imgs = os.listdir(full_pgimg_path).sort(key=alphanum_key)
    pimg = [f for f in imgs if __filter_fnames(f)]
    for f in pimg:
        csum = __csum_file(os.path.join(full_pgimg_path, f))
        fname = os.path.relpath(os.path.join(full_pgimg_path, f), full_ms_path)
        sh.write("{0} {1}\n".format(csum, fname))

    if os.path.exists(full_backup_path):
        bimgs = os.listdir(full_backup_path).sort(key=alphanum_key)
        bkup = [f for f in bimgs if __filter_fnames(f)]
        for f in bkup:
            csum = __csum_file(os.path.join(full_backup_path, f))
            fname = os.path.relpath(os.path.join(full_backup_path, f), full_ms_path)
            sh.write("{0} {1}\n".format(csum, fname))
    sh.close()

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
    """ Based on
        http://abstracthack.wordpress.com/2007/10/19/calculating-md5-checksum/
    """

    m = hashlib.sha1()  # == 'hashlib.md5' or 'hashlib.sha1'
    blocksize = 0x10000

    fd = open(filename, 'rb')
    try:
        contents = iter(lambda: fd.read(blocksize), "")
        null = [m.update(f) for f in contents]
    finally:
        fd.close()
    return m.hexdigest()

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
            retcode = subprocess.call(["/usr/local/bin/gs",
                                        "-dNOPAUSE",
                                        "-q",
                                        "-r150x150",
                                        "-sDEVICE=png16m",
                                        "-dBATCH",
                                        "-o", outfname,
                                        infname], env={"TEMP": "/home/ahankins/tmp"})
        except:
            sys.stdout.write("\trna ERROR: >>>>>> BAD PDF FILE WAS {0}\n".format(infname))
            sys.stdout.flush()
            raise(Exception)  # gettin' outta dodge

        # make a backup copy of the original PDF file
        if not os.path.exists(backup_path):
            os.mkdir(backup_path)
        os.rename(infname, os.path.join(backup_path, f))

    retval = [f for f in os.listdir(pgimg_path) if __filter_fnames(f)]
    retval.sort(key=alphanum_key)
    return retval