from lxml import html
from lxml import etree
import json
import requests
import urllib
import os
import argparse
import sys

###
### Downloads images from a fotowebcam.eu webcam. 
###


parser = argparse.ArgumentParser(description="Downloads bestof images from a fotowebcam.eu webcam")
parser.add_argument('webcam', help='the fotowebcam name')
parser.add_argument('--path', help='where to save the images, default is cwdir')

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

resolution = "_hu"
extension = ".jpg"
url = ("http://www.foto-webcam.eu/webcam/%s/" % args.webcam)


targetpath= os.dirname(args.path) if args.path else os.getcwd()
blacklistpath = os.path.join(targetpath, "blacklist")
fileslistpath = os.path.join(targetpath, "fileslist")

print ("http://www.foto-webcam.eu/webcam/include/list.php?img=&wc=%s&bestof=1" % args.webcam)

imagelist = requests.get("http://www.foto-webcam.eu/webcam/include/list.php?img=&wc=%s&bestof=1" % args.webcam)
images = json.loads(imagelist.text)

bestoflist = images['bestof']

with open(blacklistpath, 'a+') as f:
	blacklist = f.read().splitlines()

with open(fileslistpath, 'a+') as f:
	addToBlackList = f.read().splitlines()


for f in os.listdir(targetpath):
	if f in addToBlackList:
		addToBlackList.remove(f)

blacklist = blacklist + addToBlackList

    
downloaded = 0
blacklisted = 0
existing = 0
    
downloadlist = []
for i in bestoflist:
    imagename = i + resolution + extension
    imageurl = url + imagename
    filename = imagename.replace("/", "-")
    filepath = os.path.join(targetpath, filename)
    
    print "checking %s:" % imagename
    #print imageurl
    
    if os.path.isfile(filepath):
        print "\talready exists!"
        downloadlist.append(filename)
        existing = existing + 1
    elif filename in blacklist:
        print "\tblacklisted!"
        blacklisted = blacklisted + 1
    else:
        print "\tdownloading..."
        urllib.urlretrieve(imageurl, filepath)
        downloadlist.append(filename)
        downloaded = downloaded + 1
        print "\tdone"


with open(os.path.join(targetpath, 'fileslist'), 'w') as f:
	f.write("\n".join(downloadlist))

with open(blacklistpath, 'w') as f:
	f.write("\n".join(blacklist))

print ""
print "-" * 50
print "BestOf imgs available:\t%d" % len(bestoflist)
print "-" * 50
print "Downloaded: \t\t%d" % downloaded
print "Ignored: \t\t%d (blacklist: %d, existing: %d)" % (blacklisted + existing, blacklisted, existing)
if len(addToBlackList) > 0:
	print "Added to blacklist: \t%d" % len(addToBlackList)
	print "\t%s" % str(addToBlackList) 
print "-" * 50
