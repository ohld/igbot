import sqlite3


class DB(object):
    def __init__(self, db_filename):
        self.__conn = sqlite3.connect(db_filename)
        self.__conn.execute("CREATE TABLE IF NOT EXISTS 'follows' ("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "user_id TEXT NOT NULL, "
                            "username TEXT, "
                            "followed_at DATETIME NOT NULL, "
                            "unfollowed_at DATETIME)")
        self.__conn.commit()

    def record_follow(self, user_id, username=None):
        self.__conn.execute("INSERT INTO follows(user_id, username, followed_at) "
                            "VALUES (?, ?, DATETIME('now'))", [user_id, username])
        self.__conn.commit()

    def record_unfollow(self, user_id):
        self.__conn.execute("UPDATE follows "
                            "SET unfollowed_at = DATETIME('now') "
                            "WHERE user_id = ?", [user_id])
        self.__conn.commit()

    def get_followed_before(self, seconds_ago):
        cursor = self.__conn.execute(("SELECT user_id FROM follows "
                                      "WHERE unfollowed_at IS NULL "
                                      "AND followed_at < DATETIME('now', '-{} seconds')".format(seconds_ago)))
        return [row[0] for row in cursor.fetchall()]
