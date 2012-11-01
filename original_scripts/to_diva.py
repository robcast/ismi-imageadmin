import os
import sys
import shutil
import tempfile
import subprocess
import re

valid_extensions = [".pdf", ".zip", ".jpg", ".jpeg", ".tif", ".tiff", ".JPG", ".JPEG", ".TIF", ".TIFF", ".PDF", '.png', '.PNG']

def tryint(s):
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def __filter_fnames(fname):
    if fname.startswith('.'):
        return False
    if fname.startswith('_'):
        return False
    if fname == "Thumbs.db":
        return False
    if os.path.splitext(fname)[-1].lower() not in valid_extensions:
        return False
    return True


def main(args):
    indir = args["indir"]
    outdir = args["outdir"]

    sys.stdout.write("img: Converting {0}\n".format(indir))
    sys.stdout.flush()

    pgimg_path = os.path.join(indir, 'pageimg')
    ms_name = os.path.basename(indir)
    out_path = os.path.join(outdir, ms_name)

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    images = [os.path.join(pgimg_path, f) for f in os.listdir(pgimg_path) if __filter_fnames(f)]
    images.sort(key=alphanum_key)

    for image in images:
        tdir = None
        name = os.path.basename(image)
        name, ext = os.path.splitext(name)

        # some tiff files are corrupted. We'll take the safe route and convert all files, TIFF or not.

        sys.stdout.write("img: Converting {0} to TIFF\n".format(image))
        sys.stdout.flush()

        tdir = tempfile.mkdtemp(dir="/home/ahankins/tmp")
        subprocess.call(["convert",
                            "-compress", "None",
                            image,
                            os.path.join(tdir, "{0}.tiff".format(name))])

        input_file = os.path.join(tdir, "{0}.tiff".format(name))
        output_file = os.path.join(out_path, "{0}.jp2".format(name))

        sys.stdout.write("img: Converting {0} to JPEG2000\n".format(input_file))
        sys.stdout.flush()
        subprocess.call(["/bin/kdu_compress",
                            "-i", input_file,
                            "-o", output_file,
                            "-num_threads", "1",
                            "Clevels=5",
                            "Cblk={64,64}",
                            "Cprecincts={256,256},{256,256},{128,128}",
                            "Creversible=yes",
                            "Cuse_sop=yes",
                            "Corder=LRCP",
                            "ORGgen_plt=yes",
                            "ORGtparts=R",
                            "-rate", "-,1,0.5,0.25",
                        ])

        sys.stdout.write("img: Removing temporary directory {0}\n".format(tdir))
        sys.stdout.flush()
        shutil.rmtree(tdir)

    sys.stdout.write("img: Done converting {0} to {1}\n".format(indir, outdir))
    sys.stdout.flush()

if __name__ == "__main__":
    print "Starting Conversion"
    args = {
        "indir": sys.argv[1],
        "outdir": sys.argv[2]
    }
    main(args)

    print "Done."
