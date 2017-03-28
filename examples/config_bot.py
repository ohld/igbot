from instabot import Bot
bot = Bot(
    max_likes_per_day=1000,
    max_unlikes_per_day=1000,
    max_follows_per_day=350,
    max_unfollows_per_day=350,
    max_comments_per_day=100,
    max_likes_to_like=100,
    max_followers_to_follow=2000,
    min_followers_to_follow=250,
    max_following_to_follow=10000,
    min_following_to_follow=10,
    max_followers_to_following_ratio=10,
    max_following_to_followers_ratio=2,
    min_media_count_to_follow=7,
    like_delay=10,
    unlike_delay=10,
    follow_delay=30,
    unfollow_delay=30,
    comment_delay=60,
    stop_words=['order', 'shop', 'store', 'free', 'doodleartindonesia',
                'doodle art indonesia', 'fullofdoodleart', 'commission',
                'vector', 'karikatur', 'jasa', 'open']
)