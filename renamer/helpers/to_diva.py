import os
import tempfile
import subprocess
import shutil
from celery import task
from django.conf import settings
from renamer.helpers.directoryinfo import alphanum_key
from renamer.helpers.generate_json import generate_json


valid_extensions = [".pdf", ".zip", ".jpg", ".jpeg", ".tif", ".tiff", ".JPG", ".JPEG", ".TIF", ".TIFF", ".PDF", '.png', '.PNG']


@task(ignore_result=True)
def convert_to_diva(indir):
    outdir = settings.DIVA_LOCATION
    pgimg_path = os.path.join(indir, 'pageimg')
    ms_name = os.path.basename(indir)
    out_path = os.path.join(outdir, ms_name)

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    f = open(os.path.join(out_path, ".diva_conversion_in_progress"), "w")
    f.close()

    images = [os.path.join(pgimg_path, x) for x in os.listdir(pgimg_path) if __filter_fnames(x)]
    images.sort(key=alphanum_key)
    tdir = tempfile.mkdtemp(dir=settings.TMPDIR)
    for image in images:
        name = os.path.basename(image)
        name, ext = os.path.splitext(name)

        # some tiff files are corrupted, causing KDU to bail.
        # We'll take the safe route and convert all files, TIFF or not.
        tfile = os.path.join(tdir, "{0}.tiff".format(name))

        subprocess.call([settings.PATH_TO_VIPS,
                         "im_copy",
                         image,
                         tfile])

        output_file = os.path.join(out_path, "{0}.jp2".format(name))

        print("Input file: {0}".format(tfile))
        print("Output file: {0}".format(output_file))

        retcode = subprocess.call([settings.PATH_TO_KDU,
                                    "-i", tfile,
                                    "-o", output_file,
                                    "Clevels=5",
                                    "Cblk={64,64}",
                                    "Cprecincts={256,256},{256,256},{128,128}",
                                    "Creversible=yes",
                                    "Cuse_sop=yes",
                                    "Corder=LRCP",
                                    "ORGgen_plt=yes",
                                    "ORGtparts=R",
                                    "-rate", "-,1,0.5,0.25"])

        print("Generated {0}. Returned with code {1}. Continuing.".format(output_file, retcode))

    shutil.rmtree(tdir)
    os.remove(os.path.join(out_path, ".diva_conversion_in_progress"))

    print("Generating JSON.")
    generate_json.delay(out_path, settings.DATA_LOCATION)

    return True


def __filter_fnames(fname):
    if fname.startswith('.'):
        return False
    if fname == "Thumbs.db":
        return False
    if os.path.splitext(fname)[-1].lower() not in valid_extensions:
        return False
    return True
