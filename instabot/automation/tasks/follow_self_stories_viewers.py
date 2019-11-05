from instabot.automation.task import Task
from instabot.utils.list_utils.list_utils import ListUtils


class FollowSelfStoriesViewersNotFollowing(Task):
    task_id = "follow_self_stories_viewers_not_following"
    task_name = "Follow self stories viewers not following"

    def do(self):
        """Follows the viewers of my stories that are not following me"""
        story_viewers_dict = self.bot.get_self_stories_viewers()
        myfollowers = self.bot.followers
        viewers = []
        for story_id, story_dict in story_viewers_dict.items():
            for user in story_dict["users"]:
                viewers.append(str(user["pk"]))
        to_follow = ListUtils.diff(viewers, myfollowers)
        for user in to_follow:
            self.bot.follow(user)
