from . import delay


def upload_video(self, video, thumbnail, caption=''):
    delay.small_delay(self)
    self.logger.info("Started uploading '{video}'".format(video=video))
    if not self.api.upload_video(video, thumbnail, caption):
        self.logger.info("Video '%s' is not %s ." % (video, 'uploaded'))
        return False
    self.logger.info("Video '{video}' uploaded".format(video=video))
    return True
