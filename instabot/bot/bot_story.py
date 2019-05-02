def download_stories(self, username):
    user_id = self.get_user_id_from_username(username)
    list_image, list_video = self.get_user_stories(user_id)
    if list_image == [] and list_video == []:
        self.logger.error(
            "Make sure that '{}' is NOT private and that posted some stories".format(username))
        return False
    self.logger.info("Downloading stories...")
    for story_url in list_image:
        filename = story_url.split('/')[-1].split('.')[0] + ".jpg"
        self.api.download_story(filename, story_url, username)
    for story_url in list_video:
        filename = story_url.split('/')[-1].split('.')[0] + ".mp4"
        self.api.download_story(filename, story_url, username)


def upload_story_photo(self, photo, upload_id=None):
    self.small_delay()
    if self.api.upload_story_photo(photo, upload_id):
        self.logger.info("Photo '{}' is uploaded as Story.".format(photo))
        return True
    self.logger.info("Photo '{}' is not uploaded.".format(photo))
    return False
