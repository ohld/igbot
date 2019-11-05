# upload_video
Upload video. Videos will be resized and cropped (if needed) from instabot and thumbnail will be created.

## Requirements
To resize/crop/convert videos, module python `moviepy` is required. To install use:
```
pip install moviepy
```
You may need also to
```
pip install --upgrade setuptools
```
and
```
pip install numpy --upgrade --ignore-installed
```
Other system requirements will be automatically installed by python `moviepy` module itself at first usage.

## How to run
- To show help, run
```
python upload_video.py -h
```
- To upload one random video, run the script
```
python upload_video.py
```
- To upload a speficic video, run the script
```
python upload_video.py -video {video_name} -caption "{your_caption}"
```

## Settings
- videos are stored in _media_ folder
- videos can be `.mp4` and `.mov` (not tested with other formats)
- edit _captions_for_medias.py_ to add captions for video in _media_ folder
- if you don't provide a caption in _captions_for_medias.py_, the script will ask you to write it in CLI

## WARNINGS
- Videos, if needed, will be resized and cropped to
  - 90:47 (max width 1080 px) if horizontal
  - 4:5 (max height 1080 px) if vertical
  - 1:1 (1080x1080 px) if square
- After convert and cropping/resizing, a temporary video will be saved to `{video_name}.CONVERTED.mp4` in _media_ folder
- After thumbnail creation, a temporary picture will be saved to `{video_name}.jpg` in _media_ folder
- After failed upload, temporary video and thumbnail will be left in _media_ folder for debugging purposes
- After succefull upload, temporary video and tumbnail will be renamed to `{name}.REMOVE_ME` in _media_ folder
- Uploaded video names will be stored in _videos.txt_
___
_by @maxdevblock_
