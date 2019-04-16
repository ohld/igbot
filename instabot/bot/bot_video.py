import os


def upload_video(self, video, caption=''):
    self.small_delay()
    self.logger.info("Started uploading '{video}'".format(video=video))
    if not self.api.upload_video(video, caption):
        self.logger.info("Video '%s' is not %s ." % (video, 'uploaded'))
        return False
    self.logger.info("Video '{video}' uploaded".format(video=video))
    return True


def download_video(self, media_id, folder='videos', filename=None, save_description=False):
    self.small_delay()
    if not os.path.exists(folder):
        os.makedirs(folder)
    if save_description:
        media = self.get_media_info(media_id)[0]
        caption = media['caption']['text'] if media['caption'] else ''
        username = media['user']['username']
        fname = os.path.join(folder, '{}_{}.txt'.format(username, media_id))
        with open(fname, encoding='utf8', mode='w') as f:
            f.write(caption)
    try:
        return self.api.download_video(media_id, filename, False, folder)
    except Exception:
        self.logger.info("Media with `{}` is not downloaded.".format(media_id))
        return False
