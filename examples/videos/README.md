# upload_video
Upload videos. Thumbnails will be created from instabot.

## Requirements
To resize/crop videos and create thumbnails, are required on your OS
- `ffprobe` and `ffmpeg`. Tested with version `3.4.4`
- `convert` (ImageMagick). Tested with versions `7.0.8` and `6.8.9`

## How to run
- To show help, run
```
python upload_videos.py -h
```
- To upload one random video, run the script
```
python upload_videos.py
```
- To upload a speficic video, run the script
```
python upload_videos.py -video {video_name} -caption "{your_caption}"
```

## Settings
- videos are stored in _videos_ folder
- videos has to be `.mp4`
- edit _captions_for_pictures.py_ to add captions for videos in _media_ folder
- if you don't provide a caption in _captions_for_pictures.py_, the script will ask you to write it in CLI

## WARNINGS
- Videos will be resized and, if needed, cropped to
  - 16:9 (800x450 px) if horizontal
  - 4:5 (640x800 px) if vertical
  - 1:1 (800x800) if square
- Thumbnail will be created in _media_ folder with name `{video_name}.thumbnail.jpg` and removed after succesfull upload
- Original videos will be renamed to `{video_name}.ORIGINAL.{ext}.REMOVE_ME` in _media_ folder
- Uploaded video names will be stored in _videos.txt_
___
_by @maxpierini_
