# upload_photos
Upload photos. Photos will be resized and cropped (if needed) from instabot.

## Requirements
To resize/crop/convert photos, module python `Pillow` is required. To install use:
```
pip install Pillow
```

## How to run
- To show help, run
```
python upload_photos.py -h
```
- To upload one random photo, run the script
```
python upload_photos.py
```
- To upload a specific photo, run the script
```
python upload_photos.py -photo {photo_name} -caption "{your_caption}"
```

## Settings
- photos are stored in _media_ folder
- photos can be `.jpg`, `.jpeg` or `.png`
- edit _captions_for_medias.py_ to add captions for photos in _media_ folder
- if you don't provide a caption in _captions_for_medias.py_, the script will ask you to write it in CLI

## WARNINGS
- Photos will be resized and, if needed, cropped to
  - 90:47 (max width 1080 px) if horizontal
  - 4:5 (max height 1080 px) if vertical
  - 1:1 (1080x1080 px) if square
- After convert and cropping/resizing, a temporary photo be saved to `{photo_name}.CONVERTED.jpg` in _media_ folder
- After failed upload, temporary photo `{photo_name}.CONVERTED.jpg` will be left in _media_ folder for debugging purposes
- After successful upload, temporary photo will be renamed to `{photo_name}.CONVERTED.jpg.REMOVE_ME` in _media_ folder
- Uploaded pics names will be stored in _pics.txt_
___
_by @maxdevblock_
