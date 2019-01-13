# upload_photos
Upload photos. Photos will be resized and cropped (if needed) from instabot.

## Requirements
To resize/crop photos, are required on your OS:
- `convert` (ImageMagick) version `7.x`. Tested with versions `7.0.8`
  - Read here how to install `convert` https://imagemagick.org/script/download.php
- `exiftool`. Tested with version `10.10` and `11.14`
  - Read here how to install `exiftool`:
    - on Linux https://linoxide.com/linux-how-to/install-use-exiftool-linux-ubuntu-centos/
    - on Mac http://macappstore.org/exiftool/
    - on Windows https://sno.phy.queensu.ca/~phil/exiftool/install.html#Windows

## How to run
- To show help, run
```
python upload_photos.py -h
```
- To upload one random photo, run the script
```
python upload_photos.py
```
- To upload a speficic photo, run the script
```
python upload_photos.py -photo {photo_name} -caption "{your_caption}"
```

## Settings
- photos are stored in _media_ folder
- photos can be `.jpg`, `.jpeg` or `.png`
- edit _captions_for_pictures.py_ to add captions for photos in _media_ folder
- if you don't provide a caption in _captions_for_pictures.py_, the script will ask you to write it in CLI

## WARNINGS
- Photos will be resized and, if needed, cropped to
  - 90:47 (1080x609 px) if horizontal
  - 4:5 (864x1080 px) if vertical
  - 1:1 (1080x1080) if square
- Photos will converted to `.jpg`
- After convert and cropping/resizing, original photos will be renamed to `{photo_name}.{ext}.ORIGINAL` in _media_ folder
- After exiftool metadata stripping, original converted and cropped/resized photos will be renamed to `{photo_name}.TMP.jpg_original` in _media_ folder
- Uploaded pics names will be stored in _pics.txt_
___
_by @maxdevblock_
