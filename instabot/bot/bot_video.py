
def upload_video(self, video, caption=''):
    self.small_delay()
    self.logger.info("Started uploading '{video}'".format(video=video))
    if not self.api.upload_video(video, caption):
        self.logger.info("Video '%s' is not %s ." % (video, 'uploaded'))
        return False
    self.logger.info("Video '{video}' uploaded".format(video=video))
    return True
