"""
A script for downloading best-of images from www.fotowebcam.eu
"""
import argparse
import json
import urllib.request as urllib
import os
import sys
import requests
from tqdm import tqdm

IMAGE_URL_PATTERN = "http://www.foto-webcam.eu/webcam/{}/"
BESTOF_URL_PATTERN = "http://www.foto-webcam.eu/webcam/include/thumb.php?wc={}&mode=bestof&page={}"
BLACKLIST_PATH_PATTERN = ".{}.blacklist"
RESOLUTION = "_hu"
EXTENSION = ".jpg"
PATH = os.getcwd()

class TqdmUpTo(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def print_result(nr_bestofimages, nr_downloaded, nr_blacklisted, nr_existing, nr_failed):
    """
    Print the result.
    """
    print("")
    print("-" * 75)
    print("# of best-of images:\t%d" % nr_bestofimages)
    print("-" * 75)
    print("Downloaded: \t\t%d" % nr_downloaded)
    print("Failed: \t\t%d" % nr_failed)
    print("Ignored: \t\t%d (blacklist: %d, existing: %d)" % (nr_blacklisted + nr_existing,
                                                             nr_blacklisted, nr_existing))

    sys.stdout.flush()

def parse_args():
    parser = argparse.ArgumentParser(
        description="Downloads bestof images from a fotowebcam.eu webcam")
    parser.add_argument('webcam', help='one or more webcam names', nargs="*")
    parser.add_argument('--path', help='where to save the images, default is cwdir')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if (args.path):
        PATH = os.dirname(args.path)

    return args

def read_blacklist(name):
    blacklist_file = os.path.join(PATH, BLACKLIST_PATH_PATTERN.format(name))
    if os.path.exists(blacklist_file):
        with open(blacklist_file, 'r') as blacklist:
            return blacklist.read().splitlines()
    else:
        return []

def load_imagelist(name):
    page = 0
    imgs = []

    while True:
        imagelist = requests.get(BESTOF_URL_PATTERN.format(name, page))
        images = json.loads(imagelist.text)['images']
        if len(images) <= 0:
            break
        imgs.extend(images)
        page += 1

    return imgs 

def update_blacklist(cache):
    add_to_blacklist = list(cache["files"])
    for file_name in os.listdir(PATH):
        if file_name in add_to_blacklist:
            add_to_blacklist.remove(file_name)

    cache["blacklist"].append(add_to_blacklist)
    return add_to_blacklist

def download(name, bestoflist, blacklist):
    nr_downloaded = nr_blacklisted = nr_existing = nr_failed = 0
    for i in bestoflist:
        imagename = i + RESOLUTION + EXTENSION
        imageurl = IMAGE_URL_PATTERN.format(name) + imagename

        filename = imagename.replace("/", "-")
        filepath = os.path.join(PATH, "{}_{}".format(name, filename))

        print("checking %s:" % imagename)

        if filename in blacklist:
            print("\tblacklisted!")
            nr_blacklisted += 1
        elif os.path.isfile(filepath):
            print("\talready exists!")
            nr_existing += 1
        else:
            with TqdmUpTo(unit='B', unit_scale=True, miniters=1) as t:
                try:
                    urllib.urlretrieve(imageurl, filepath, reporthook=t.update_to)
                    nr_downloaded += 1
                    print("\tdone")
                except:
                    print("\tDownload failed!")
                    nr_failed += 1
            
        sys.stdout.flush()

    return (nr_downloaded, nr_blacklisted, nr_existing, nr_failed)

def main():
    args = parse_args()

    for webcam in args.webcam:
        print("-" * 50)
        print(webcam)
        bestoflist = load_imagelist(webcam)
        blacklist = read_blacklist(webcam)

        (nr_downloaded, nr_blacklisted, nr_existing, nr_failed) = download(webcam, bestoflist, blacklist)
        print_result(len(bestoflist), nr_downloaded, nr_blacklisted, nr_existing, nr_failed)

if __name__ == "__main__":
    main()
    