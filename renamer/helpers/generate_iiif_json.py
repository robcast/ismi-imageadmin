#!/usr/bin/env python

# Copyright (C) 2013 by Andrew Hankinson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import os
import re
import math
import sys
import json
try:
    from django.conf import settings
except:
    pass
# fix UUID problem
import uuid
uuid._uuid_generate_random = None

from celery import task


@task(ignore_result=True)
def generate_json(indir, outdir):
    gen = GenerateIiifJson(indir, outdir)
    res = gen.generate()
    print("Generate Json returned: {0}".format(res))


class GenerateIiifJson(object):
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.title = os.path.basename(self.input_directory)

    def generate(self):
        self.__generate()
        return True

    def __generate(self):
        img_dir = self.input_directory

        files = os.listdir(img_dir)
        files.sort(key=self.__alphanum_key)  # sort alphabetical, not asciibetical
        lowest_max_zoom = 0
        zoomlevels = []
        images = []

        for i, f in enumerate(files):
            ignore, ext = os.path.splitext(f)
            if f.startswith("."):
                continue    # ignore hidden files

            if ext in ('.jp2', '.jpx'):
                width, height = self.__img_size_jp2(os.path.join(img_dir, f))
            elif ext in ('.tiff', '.tif'):
                width, height = self.__img_size_tiff(os.path.join(img_dir, f))
            else:
                continue    # ignore anything else.

            canvas_uri = "%s/%s/canvas/%s"%(settings.IIIF_MANIF_BASE_URL, self.title, i)
            image_uri = "%s/%s/image/%s"%(settings.IIIF_MANIF_BASE_URL, self.title, f)
            image_service_uri = "%s/%s"%(settings.IIIF_IMAGE_BASE_URL, f)

            iiif_images = {
                '@type': 'oa:Annotation',
                'motivation': 'sc:painting',
                'resource': {
                    '@id': image_uri,
                    '@type': 'dctypes:Image',
                    'service': {
                        '@context': 'http://iiif.io/api/image/2/context.json',
                        '@id': image_service_uri,
                        'profile': 'http://iiif.io/api/image/2/level1.json'
                    },
                    'height': height,
                    'width': width
                },
                'on': canvas_uri
            }

            iiif_canvas = {
                '@context': 'http://iiif.io/api/presentation/2/context.json',
                '@id': canvas_uri,
                '@type': 'sc:Canvas',
                'label': "Scan No %s"%i,
                'width': width,
                'height': height,
                'images': iiif_images 
            }
            
            images.append(iiif_canvas)


        manifest_uri = "%s/%s/manifest"%(settings.IIIF_MANIF_BASE_URL, self.title)
        sequence_uri = "%s/%s/sequence/default"%(settings.IIIF_MANIF_BASE_URL, self.title)

        data = {
            '@context': 'http://iiif.io/api/presentation/2/context.json',
            '@type': 'sc:Manifest',
            '@id': manifest_uri,
            'label': "[%s]"%self.title,
            'description': "[Scanned document %s]"%self.title,
            'sequences': [ {
                '@id': 'http://example.org/iiif/book1/sequence/normal',
                '@type': 'sc:Sequence',
                'label': 'Default scan order',
                'viewingHint': 'paged',
                'canvases': images
            } ]
        }

        # write the JSON out to a file in the output directory
        f = open(os.path.join(self.output_directory, "{0}.json".format(self.title)), 'w')
        json.dump(data, f)
        f.close()

    def __img_size_jp2(self, fn):
        # we implement our own header reader since all the existing
        # JPEG2000 libraries seem to read the entire image in, and they're
        # just tooooo sloooowww.
        f = open(fn, 'rb')
        d = f.read(100)
        startHeader = d.find('ihdr')
        hs = startHeader + 4
        ws = startHeader + 8
        height = ord(d[hs]) * 256 ** 3 + ord(d[hs + 1]) * 256 ** 2 + ord(d[hs + 2]) * 256 + ord(d[hs + 3])
        width = ord(d[ws]) * 256 ** 3 + ord(d[ws + 1]) * 256 ** 2 + ord(d[ws + 2]) * 256 + ord(d[ws + 3])
        f.close()
        return (width, height)

    def __img_size_tiff(self, fn):
        # We can use the VIPS module here for TIFF, since it can handle all the
        # ins and outs of the TIFF image format quite nicely.

        # if we're not dealing with TIFF, we don't need to import a non-core library.
        # Since jpeg2000 works by reading the header directly, we've made the choice to
        # import this with every call. It's not ideal, but it shouldn't be too bad.
        # If you are dealing with TIFF files and want to make a slight optimization you
        # can move this import statement to the top of this script.
        from vipsCC import VImage
        im = VImage.VImage(fn)
        size = (im.Xsize(), im.Ysize())
        del im
        return size

    def __tryint(self, s):
        try:
            return int(s)
        except:
            return s

    def __alphanum_key(self, s):
        """ Turn a string into a list of string and number chunks.
            "z23a" -> ["z", 23, "a"]
        """
        return [self.__tryint(c) for c in re.split('([0-9]+)', s)]


if __name__ == "__main__":
    from optparse import OptionParser
    # fake Django settings
    class settings(object): 
        IIIF_IMAGE_BASE_URL = 'http://example.com/iiif/image'
        IIIF_MANIF_BASE_URL = 'http://example.com/iiif/presentation'

    usage = "%prog [options] input_directory output_directory"
    parser = OptionParser(usage)
    options, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        parser.error("You must specify a directory to process.")

    opts = {
        'input_directory': args[0],
        'output_directory': args[1]
    }

    gen = GenerateIiifJson(**opts)
    sys.exit(gen.generate())
