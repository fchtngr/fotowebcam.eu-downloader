# Foto-Webcam.eu Downloader

A python script for downloading best-of images from 'foto-webcam.eu'. 

Foto-Webcam.eu produces some great high-res photos and the community is marking the best ones. However, manually downloading them was too tedious so I wrote this script. 

I use it for downloading 'https://www.foto-webcam.eu/webcam/traunstein/' and using the images as desktop background.

## Usage

```
$ python fotowebcam-dl.py -h
usage: fotowebcam-dl.py [-h] [--path PATH] webcam

Downloads bestof images from a fotowebcam.eu webcam

positional arguments:
  webcam       the fotowebcam name

optional arguments:
  -h, --help   show this help message and exit
  --path PATH  where to save the images, default is cwdir
```

You can blacklist fotos by simply deleting it from the download folder (not all best-of fotos are really the "best" ;)). Next time you invoke the downloader the deleted file will be added to the blacklist.

## Sample Output

```
> python fotowebcam-dl.py traunstein
checking 2017/01/20/0840_hu.jpg:
        downloading...
        done
checking 2017/01/10/1620_hu.jpg:
        downloading...
        done
checking 2016/06/15/1820_hu.jpg:
        already exists!
checking 2015/10/05/1630_hu.jpg:
        blacklisted!
[...]

--------------------------------------------------
BestOf imgs available:  112
--------------------------------------------------
Downloaded:             21
Ignored:                91 (blacklist: 11, existing: 80)
Added to blacklist:     1
        ['2016-05-21-1100_hu.jpg']
--------------------------------------------------
```