# helper methods for the views module for getting
# the various directory listings.
import os
import re


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


def _filter_fnames(fname):
    if fname.startswith("."):
        return False
    else:
        return True


def list_directory(thisdir):
    dirs = [f for f in os.listdir(thisdir) if _filter_fnames(f)]
    dirs.sort(key=alphanum_key)
    return dirs


def check_difference(dir1, dir2):
    """
        Checks to see if all the directories in dir1
        also exist in dir2. Returns a list of the
        directories that do not match.
    """
    d1 = set(dir1)
    d2 = set(dir2)
    return list(d1.difference(d2))


def check_intersection(dir1, dir2):
    d1 = set(dir1)
    d2 = set(dir2)
    return list(d1.intersection(d2))
