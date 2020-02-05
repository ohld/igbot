def download_stories(self, username):
    user_id = self.get_user_id_from_username(username)
    list_image, list_video = self.get_user_stories(user_id)
    if list_image == [] and list_video == []:
        self.logger.error(
            (
                "Make sure that '{}' is NOT private and that " "posted some stories"
            ).format(username)
        )
        return False
    self.logger.info("Downloading stories...")
    for story_url in list_image:
        filename = story_url.split("/")[-1].split(".")[0] + ".jpg"
        self.api.download_story(filename, story_url, username)
    for story_url in list_video:
        filename = story_url.split("/")[-1].split(".")[0] + ".mp4"
        self.api.download_story(filename, story_url, username)


def upload_story_photo(self, photo, upload_id=None):
    self.small_delay()
    if self.api.upload_story_photo(photo, upload_id):
        self.logger.info("Photo '{}' is uploaded as Story.".format(photo))
        return True
    self.logger.info("Photo '{}' is not uploaded.".format(photo))
    return False


def watch_users_reels(self, user_ids, max_users=100):
    """
        user_ids - the list of user_id to get their stories
        max_users - max amount of users to get stories from.

        It seems like Instagram doesn't allow to get stories
        from more that 100 users at once.
    """

    # In case of only one user were passed
    if not isinstance(user_ids, list):
        user_ids = [user_ids]

    # Get users reels
    reels = self.api.get_users_reel(user_ids[:max_users])

    # Filter to have users with at least 1 reel
    if isinstance(reels, list):
        # strange output
        return False

    reels = {k: v for k, v in reels.items() if "items" in v and len(v["items"]) > 0}

    # Filter reels that were not seen before
    unseen_reels = []
    for _, reels_data in reels.items():
        last_reel_seen_at = reels_data["seen"] if "seen" in reels_data else 0
        unseen_reels.extend(
            [r for r in reels_data["items"] if r["taken_at"] > last_reel_seen_at]
        )

    # See reels that were not seen before
    # TODO: add counters for watched stories
    if self.api.see_reels(unseen_reels):
        self.total["stories_viewed"] += len(unseen_reels)
        return True
    return False
