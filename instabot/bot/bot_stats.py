import os
import datetime


def get_tsv_line(dictionary):
    line = ""
    for key in sorted(dictionary):
        line += str(dictionary[key]) + "\t"
    return line[:-2] + "\n"


def get_header_line(dictionary):
    line = "\t".join(dictionary)
    return line + "\n"


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory) and len(directory) > 0:
        os.makedirs(directory)


def dump_data(data, path):
    ensure_dir(path)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(get_header_line(data))
            f.write(get_tsv_line(data))
    else:
        with open(path, "a") as f:
            f.write(get_tsv_line(data))


def save_user_stats(self, username, path=""):
    user_id = self.convert_to_user_id(username)
    infodict = self.get_user_info(user_id)
    if infodict:
        data_to_save = {}
        data_to_save["date"] = str(datetime.datetime.now())
        data_to_save["followers"] = int(infodict["follower_count"])
        data_to_save["following"] = int(infodict["following_count"])
        data_to_save["medias"] = int(infodict["media_count"])
        file_path = os.path.join(path, "%s.tsv" % username)
        dump_data(data_to_save, file_path)
    self.logger.info("Stats saved at %s." % data_to_save["date"])
    return False
