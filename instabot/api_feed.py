import requests
import json
import time, datetime
import random
import sys
from tqdm import tqdm

def get_feed(self, amount):
    print ("Getting %d medias from your current feed"%(amount))
    response = self.post('https://www.instagram.com/query/',      {
      'q': '''ig_me() {
              feed {
                media.first(20) {
                  nodes {
                    id, attribution, caption,
                    code, display_src, is_video,
                    likes {
                      count, viewer_has_liked
                    },
                    location {
                      id, has_public_page, name, slug
                    },
                    owner {
                      id, username,
                      blocked_by_viewer, requested_by_viewer,
                      followed_by_viewer, full_name,
                      has_blocked_viewer, is_private
                    },
                    video_views
                  },
                  page_info
                }
              },
              id,
              username
      }''',
      'ref': 'feed::show',
      'query_id': '%d'%random.randint(0, 99999999999)
    })

    if response.status_code != 200:
        return False
    data = response.json()

    if "media" not in data["feed"]:
        print ("  Can't get feed.")
        return []
    elif "nodes" not in data["feed"]["media"]:
        print ("  You have no feed.")
        return []

    feed_media = data["feed"]["media"]["nodes"]
    if len(feed_media) >= amount:
        return feed_media

    with tqdm(total=amount) as pbar:
        pbar.update(len(feed_media))
        while len(feed_media) < amount and data["feed"]["media"]["page_info"]["has_next_page"]:
            time.sleep(3 * random.random())
            cursor = data["feed"]["media"]["page_info"]["end_cursor"]
            response = self.post('https://www.instagram.com/query/', {
                'q': '''ig_me() {
                        feed {
                          media.after(%s, 20) {
                            nodes {
                              id, attribution, caption,
                              code, display_src, is_video,
                              likes {
                                count, viewer_has_liked
                              },
                              location {
                                id, has_public_page, name, slug
                              },
                              owner {
                                id, username,
                                blocked_by_viewer, requested_by_viewer,
                                followed_by_viewer, full_name,
                                has_blocked_viewer, is_private
                              },
                              video_views
                            },
                            page_info
                          }
                        },
                        id,
                        username
                }'''%(cursor),
                'ref': 'feed::show',
                'query_id': '%d'%random.randint(0, 99999999999)
            })

            if response.status_code != 200:
                print ("Error while requesting more feed")
                return feed_media
            data = response.json()
            pbar.update(len(data["feed"]["media"]["nodes"]))
            feed_media.extend(data["feed"]["media"]["nodes"])
    return feed_media
