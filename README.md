# Foto-Webcam.eu Downloader

A python script for downloading best-of images from 'foto-webcam.eu'. 

Foto-Webcam.eu produces some great high-res photos and the community is marking the best ones. However, manually downloading them was too tedious so I wrote this script. 

I use it for downloading 'https://www.foto-webcam.eu/webcam/traunstein/' and using the images as desktop background.

## Usage

```
$ python fotowebcam-dl.py -h
usage: fotowebcamdl.py [-h] [--path PATH] [webcam [webcam ...]]

Downloads bestof images from a fotowebcam.eu webcam

positional arguments:
  webcam       one or more webcam names

optional arguments:
  -h, --help   show this help message and exit
  --path PATH  where to save the images, default is cwdir
```

You can blacklist photos simply by adding the filename to a `<webcam>`.blacklist file (not all best-of photos are really the "best" ;)). Next time you invoke the downloader those images won't be downloaded again. All files will be prefixed with the `<webcam>_` name. When blacklisting, omit the prefix.

```
> python fotowebcam-dl.py traunstein
> python fotowebcam-dl.py traunstein traunstein-sued
```