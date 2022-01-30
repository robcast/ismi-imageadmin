import os
import tempfile
import subprocess
import shutil
import logging
import io
from celery import shared_task
from django.conf import settings
from imageadmin.helpers.directoryinfo import alphanum_key
from imageadmin.helpers.generate_iiif_json import generate_json


VALID_EXTENSIONS = [".pdf", ".zip", ".jpg", ".jpeg", ".tif", ".tiff", ".JPG", ".JPEG", ".TIF", ".TIFF", ".PDF", '.png', '.PNG']

@shared_task(ignore_result=False)
def convert_to_diva(indir):
    # create logger that logs to string that can be returned by celery
    logger, log_string = _create_string_logger('imageadmin.helpers.convert_to_diva')

    logger.debug(f"starting convert to diva for {indir}")
    
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

        logger.debug("convert input file: {0}".format(image))
        logger.debug("convert output file: {0}".format(tfile))

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

        logger.debug("kdu input file: {0}".format(tfile))
        logger.debug("kdu output file: {0}".format(output_file))

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
            logger.debug("kdu generated {0}. Returned with code {1}. Continuing.".format(output_file, retcode))

        else:
            # an encoding problem
            logger.debug("kdu ERROR code {1} on file {0}.".format(output_file, retcode))
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
                logger.debug(" kdu converting {0} as sLUM.".format(output_file,))
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
                logger.debug("kdu converting {0} as sRGB.".format(output_file,))
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
                logger.debug("kdu re-generated {0}. Returned with code {1}. Continuing.".format(output_file, result.returncode))
            else:
                logger.error("kdu tried to re-generate {0}. Returned with code {1}. Continuing.".format(output_file, result.returncode))
            
    shutil.rmtree(tdir)
    os.remove(os.path.join(out_path, ".diva_conversion_in_progress"))

    logger.debug(f"Generating JSON in {out_path}")
    generate_json.delay(out_path, settings.DATA_LOCATION)

    log_contents = log_string.getvalue()
    log_string.close()
    return log_contents


def _filter_fnames(fname):
    if fname.startswith('.'):
        return False
    if fname == "Thumbs.db":
        return False
    if os.path.splitext(fname)[-1].lower() not in VALID_EXTENSIONS:
        return False
    return True

def _create_string_logger(logname):
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    log_string = io.StringIO()
    sh = logging.StreamHandler(log_string)
    #sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    return logger, log_string
