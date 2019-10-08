import os


def upload_video(self, video, caption="", thumbnail=None, options={}):
    """Upload video to Instagram

    @param video      Path to video file (String)
    @param caption    Media description (String)
    @param thumbnail  Path to thumbnail for video (String). When None, then
                      thumbnail is generate automatically
    @param options    Object with difference options, e.g. configure_timeout,
                      rename_thumbnail, rename (Dict)
                      Designed to reduce the number of function arguments!

    @return           Object with state of uploading to Instagram (or False)
    """
    self.small_delay()
    self.logger.info("Started uploading '{video}'".format(video=video))
    result = self.api.upload_video(
        video, caption=caption, thumbnail=thumbnail, options=options
    )
    if not result:
        self.logger.info("Video '{}' is not {} .".format(video, "uploaded"))
        return False
    self.logger.info("Video '{video}' uploaded".format(video=video))
    return result


def download_video(
    self, media_id, folder="videos", filename=None, save_description=False
):
    self.small_delay()
    if not os.path.exists(folder):
        os.makedirs(folder)
    if save_description:
        media = self.get_media_info(media_id)[0]
        caption = media["caption"]["text"] if media["caption"] else ""
        username = media["user"]["username"]
        fname = os.path.join(folder, "{}_{}.txt".format(username, media_id))
        with open(fname, encoding="utf8", mode="w") as f:
            f.write(caption)
    try:
        return self.api.download_video(media_id, filename, False, folder)
    except Exception:
        self.logger.info("Media with `{}` is not downloaded.".format(media_id))
        return False
