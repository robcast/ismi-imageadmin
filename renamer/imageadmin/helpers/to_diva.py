import os
import tempfile
import subprocess
import shutil
import logging
from celery import shared_task
from django.conf import settings
from imageadmin.helpers.directoryinfo import alphanum_key
from imageadmin.helpers.generate_iiif_json import generate_json


valid_extensions = [".pdf", ".zip", ".jpg", ".jpeg", ".tif", ".tiff", ".JPG", ".JPEG", ".TIF", ".TIFF", ".PDF", '.png', '.PNG']


@shared_task(ignore_result=True)
def convert_to_diva(indir):
    logging.debug(f"starting convert to diva for {indir}")
    outdir = settings.DIVA_LOCATION
    pgimg_path = os.path.join(indir, 'pageimg')
    ms_name = os.path.basename(indir)
    out_path = os.path.join(outdir, ms_name)

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    f = open(os.path.join(out_path, ".diva_conversion_in_progress"), "w")
    f.close()

    images = [os.path.join(pgimg_path, x) for x in os.listdir(pgimg_path) if _filter_fnames(x)]
    images.sort(key=alphanum_key)
    tdir = tempfile.mkdtemp(dir=settings.TMPDIR)
    for image in images:
        name = os.path.basename(image)
        name, ext = os.path.splitext(name)

        # some tiff files are corrupted, causing KDU to bail.
        # We'll take the safe route and convert all files, TIFF or not.
        tfile = os.path.join(tdir, "{0}.tiff".format(name))

        logging.debug("convert input file: {0}".format(image))
        logging.debug("convert output file: {0}".format(tfile))

        subprocess.run([settings.PATH_TO_GM,
                        "convert",
                        "-compress",  "None",
                        image,
                        tfile])

        # subprocess.call([settings.PATH_TO_VIPS,
        #                  "im_copy",
        #                  image,
        #                  tfile])

        output_file = os.path.join(out_path, "{0}.jp2".format(name))

        logging.debug("kdu input file: {0}".format(tfile))
        logging.debug("kdu output file: {0}".format(output_file))

        result = subprocess.run([settings.PATH_TO_KDU,
                                    "-i", tfile,
                                    "-o", output_file,
                                    "-num_threads", "2",
                                    "Clevels=5",
                                    "Cblk={64,64}",
                                    "Cprecincts={256,256},{256,256},{128,128}",
                                    "Creversible=yes",
                                    "Cuse_sop=yes",
                                    "Corder=LRCP",
                                    "ORGgen_plt=yes",
                                    "ORGtparts=R",
                                    "-rate", "-,1,0.5,0.25"])

        retcode = result.returncode
        if retcode == 0:
            logging.debug("kdu generated {0}. Returned with code {1}. Continuing.".format(output_file, retcode))

        else:
            # an encoding problem
            logging.debug("kdu ERROR code {1} on file {0}.".format(output_file, retcode))
            # get image info
            result = subprocess.run([settings.PATH_TO_GM,
                                     "identify",
                                     "-verbose",
                                     image,
                                     tfile],
                                     capture_output=True)
            
            info = result.stdout
            if info is not None and 'JPEG-Colorspace-Name: GRAYSCALE' in info.decode(errors='ignore'):
                # process using sLUM colorspace for grayscale
                logging.debug(" kdu converting {0} as sLUM.".format(output_file,))
                result = subprocess.run([settings.PATH_TO_KDU,
                                         "-i", tfile,
                                         "-o", output_file,
                                         "-num_threads", "2",
                                         "Clevels=5",
                                         "Cblk={64,64}",
                                         "Cprecincts={256,256},{256,256},{128,128}",
                                         "Creversible=yes",
                                         "Cuse_sop=yes",
                                         "Corder=LRCP",
                                         "ORGgen_plt=yes",
                                         "ORGtparts=R",
                                         "-rate", "-,1,0.5,0.25",
                                         "-jp2_space", "sLUM"])

            else:
                # process using sRGB colorspace for color
                logging.debug("kdu converting {0} as sRGB.".format(output_file,))
                result = subprocess.run([settings.PATH_TO_KDU,
                                         "-i", tfile,
                                         "-o", output_file,
                                         "-num_threads", "2",
                                         "Clevels=5",
                                         "Cblk={64,64}",
                                         "Cprecincts={256,256},{256,256},{128,128}",
                                         "Creversible=yes",
                                         "Cuse_sop=yes",
                                         "Corder=LRCP",
                                         "ORGgen_plt=yes",
                                         "ORGtparts=R",
                                         "-rate", "-,1,0.5,0.25",
                                         "-jp2_space", "sRGB"])
                
            if result.returncode == 0:
                logging.debug("kdu re-generated {0}. Returned with code {1}. Continuing.".format(output_file, result.returncode))
            else:
                logging.error("kdu tried to re-generate {0}. Returned with code {1}. Continuing.".format(output_file, result.returncode))
            
    shutil.rmtree(tdir)
    os.remove(os.path.join(out_path, ".diva_conversion_in_progress"))

    logging.debug(f"Generating JSON in {out_path}")
    generate_json.delay(out_path, settings.DATA_LOCATION)

    return True


def _filter_fnames(fname):
    if fname.startswith('.'):
        return False
    if fname == "Thumbs.db":
        return False
    if os.path.splitext(fname)[-1].lower() not in valid_extensions:
        return False
    return True