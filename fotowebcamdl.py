"""
A script for downloading best-of images from www.fotowebcam.eu
"""
import argparse
import json
import urllib.request as urllib
import os
import sys
import requests

IMAGE_URL_PATTERN = "http://www.foto-webcam.eu/webcam/%s/"
BESTOF_URL_PATTERN = "http://www.foto-webcam.eu/webcam/include/list.php?img=&wc=%s&bestof=1"
CACHE_PATH_PATTERN = ".%s_cache.json"
RESOLUTION = "_hu"
EXTENSION = ".jpg"
PATH = os.getcwd()

def print_result(nr_bestofimages, nr_downloaded, nr_blacklisted, nr_existing, added_to_blacklist):
    """
    Print the result.
    """
    print("")
    print("-" * 75)
    print("# of best-of images:\t%d" % nr_bestofimages)
    print("-" * 75)
    print("Downloaded: \t\t%d" % nr_downloaded)
    print("Ignored: \t\t%d (blacklist: %d, existing: %d)" % (nr_blacklisted + nr_existing,
                                                             nr_blacklisted, nr_existing))
    if len(added_to_blacklist) > 0:
        print("Added to blacklist: \t%d" % len(added_to_blacklist))
        print("\t%s" % str(added_to_blacklist))
    print("-" * 75)
    sys.stdout.flush()

def parse_args():
    parser = argparse.ArgumentParser(
        description="Downloads bestof images from a fotowebcam.eu webcam")
    parser.add_argument('webcam', help='the fotowebcam name')
    parser.add_argument('--path', help='where to save the images, default is cwdir')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if (args.path):
        PATH = os.dirname(args.path)

    return args

def write_cache(name, cache):
    cache_file = os.path.join(PATH, (CACHE_PATH_PATTERN % name))
    with open(cache_file, 'w') as cache_file:
        cache_file.write(json.dumps(cache))

def read_cache(name):
    cache_file = os.path.join(PATH, (CACHE_PATH_PATTERN % name))
    with open(cache_file, 'r') as cache_file:
        cache = json.loads(cache_file.read())
    return cache

def load_imagelist(name):
    imagelist = requests.get(BESTOF_URL_PATTERN % name)
    images = json.loads(imagelist.text)
    return images['bestof']

def update_blacklist(cache):
    add_to_blacklist = list(cache["files"])
    for file_name in os.listdir(PATH):
        if file_name in add_to_blacklist:
            add_to_blacklist.remove(file_name)

    cache["blacklist"].append(add_to_blacklist)
    return add_to_blacklist

def download(name, bestoflist, cache):
    nr_downloaded = nr_blacklisted = nr_existing = 0
    downloadlist = []
    for i in bestoflist:
        imagename = i + RESOLUTION + EXTENSION
        imageurl = (IMAGE_URL_PATTERN % name) + imagename

        filename = imagename.replace("/", "-")
        filepath = os.path.join(PATH, filename)

        print("checking %s:" % imagename)

        if os.path.isfile(filepath):
            print("\talready exists!")
            downloadlist.append(filename)
            nr_existing += 1
        elif filename in cache["blacklist"]:
            print("\tblacklisted!")
            nr_blacklisted += 1
        else:
            print("\tdownloading...")
            urllib.urlretrieve(imageurl, filepath)
            downloadlist.append(filename)
            nr_downloaded += 1
            print("\tdone")
        sys.stdout.flush()

    cache["files"] = downloadlist

    return (nr_downloaded, nr_blacklisted, nr_existing)

def main():
    args = parse_args()

    bestoflist = load_imagelist(args.webcam)

    cache = read_cache(args.webcam)
    added_to_blacklist = update_blacklist(cache)

    (nr_downloaded, nr_blacklisted, nr_existing) = download(args.webcam, bestoflist, cache)

    write_cache(args.webcam, cache)
    print_result(len(bestoflist), nr_downloaded, nr_blacklisted, nr_existing, added_to_blacklist)

if __name__ == "__main__":
    main()
    