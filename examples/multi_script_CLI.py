import getpass
import os
import random
import sys
import time

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot


# initial

def initial_checker():
    files = [hashtag_file, users_file, whitelist, blacklist, comment, setting]
    try:
        for f in files:
            with open(f, 'r') as f:
                pass
    except BaseException:
        for f in files:
            with open(f, 'w') as f:
                pass
        print("""
        Selamat datang di instabot, sepertinya ini adalah pertama kalinya Anda menggunakan bot ini.
        Sebelum memulai, mari atur dasar-dasarnya.
         Jadi bot berfungsi seperti yang Anda inginkan. BY E??KA
        """)
        setting_input()
        print("""
        Anda dapat menambahkan basis data hashtag, basis data pesaing,
        daftar putih, daftar hitam dan juga menambahkan pengguna di menu pengaturan.
        Bersenang-senang dengan bot!. BY E??KA
        """)
        time.sleep(5)
        os.system('cls')


def read_input(f, msg, n=None):
    if n is not None:
        msg += " (masukkan untuk menggunakan nomor standar: {})".format(n)
    print(msg)
    entered = sys.stdin.readline().strip() or str(n)
    if isinstance(n, int):
        entered = int(entered)
    f.write(str(entered) + "\n")


# setting function start here
def setting_input():
    inputs = [("Berapa banyak suka yang ingin Anda lakukan dalam sehari? ", 1000),
               ("Bagaimana kalau Unlike", 1000),
               ("Berapa banyak pengikut yang ingin Anda lakukan dalam sehari?", 350),
               ("Bagaimana kalau berhenti mengikuti?", 350),
               ("Berapa banyak komentar yang ingin Anda lakukan dalam sehari?", 100),
              (("Suka maksimal di media yang Anda sukai? \n"
                "Kami akan melewati media yang memiliki nilai suka lebih besar dari ini"), 100),
              (("Pengikut akun maksimal yang ingin Anda ikuti? \n"
                "Kami akan melewati media yang memiliki pengikut lebih besar dari nilai ini"), 2000),
              (("Minimum pengikut yang harus dimiliki akun sebelum kita ikuti? \n"
                "Kami akan melewati media yang memiliki pengikut lebih sedikit dari nilai ini"), 10),
              (("Maksimum mengikuti akun yang ingin Anda ikuti? \n"
                "Kami akan melewati media yang memiliki pengikut lebih besar dari nilai ini"), 7500),
              (("Minimum akun yang ingin Anda ikuti? \n"
                "Kami akan melewati media yang memiliki pengikut lebih sedikit dari nilai ini"), 10),
               ("Pengikut maksimal hingga following_ratio", 10),
               ("Mengikuti maksimal ke followers_ratio", 2),
              (("Minimal media yang akan Anda ikuti dengan akun. \n"
                "Kami akan melewati media yang memiliki lebih sedikit media dari nilai ini"), 3),
               ("Tunda dari satu suka ke yang lain seperti kamu akan tampil", 10),
               ("Keterlambatan dari satu ke yang lain tidak seperti Anda akan tampil", 10),
               ("Tunda dari satu tindak ke tindak berikutnya Anda akan melakukan", 30),
               ("Tunda dari satu berhenti ikuti ke berhenti ikuti lagi yang akan Anda lakukan", 30),
               ("Tunda dari satu komentar ke komentar lain yang akan Anda tampilkan", 60),
               ("Ingin menggunakan proxy? Masukkan proxy Anda atau biarkan kosong jika tidak. (Cukup masukkan", 'Tidak Ada')]

    with open(setting, "w") as f:
        while True:
            for msg, n in inputs:
                read_input(f, msg, n)
            break
        print("Selesai dengan semua pengaturan!")


def parameter_setting():
    settings = ["Max suka per hari:",
                 "Max tidak suka per hari:",
                 "Maks mengikuti setiap hari:",
                 "Max unfollows per hari:",
                 "Maks komentar per hari:",
                 "Max suka:",
                 "Maks pengikut untuk diikuti:",
                 "Min pengikut untuk diikuti:",
                 "Maks mengikuti untuk mengikuti:",
                 "Min mengikuti untuk mengikuti:",
                 "Maks pengikut ke following_ratio:",
                 "Maks mengikuti pengikut_ratio:",
                 "Min media_count untuk diikuti:",
                 "Seperti penundaan:",
                 "Tidak seperti penundaan:",
                 "Ikuti penundaan:",
                 "Batalkan berhenti ikuti:",
                 "Penundaan komentar:",
                 "Proxy:"]

    with open(setting) as f:
        data = f.readlines()

    print("Parameter saat ini\n")
    for s, d in zip(settings, data):
        print(s + d)


def username_adder():
    with open(SECRET_FILE, "a") as f:
        print("Kami akan menambahkan akun instagram Anda.")
        print("Jangan khawatir. Ini akan disimpan secara lokal.")
        while True:
            print("Masukkan Nama Pengguna Anda: ")
            f.write(str(sys.stdin.readline().strip()) + ":")
            print("Masukkan kata sandi Anda: ")
            f.write(getpass.getpass() + "\n")
            print("Apakah Anda ingin menambahkan akun lain? (y/n)")
            print("SCRIPT BY : E??KA")
            if "y" not in sys.stdin.readline():
                break


def get_adder(name, fname):
    def _adder():
        print("Database saat ini:")
        print(bot.read_list_from_file(fname))
        with open(fname, "a") as f:
            print('Tambahkan {} ke basis data'.format(name))
            while True:
                print("Enter {}: ".format(name))
                f.write(str(sys.stdin.readline().strip()) + "\n")
                print("Apakah Anda ingin menambahkan yang lain {}? (y/n)\n".format(name))
                if "y" not in sys.stdin.readline():
                    print('Selesai menambahkan {} ke basis data'.format(name))
                    break
    return _adder()


def hashtag_adder():
    return get_adder('hashtag', fname=hashtag_file)


def competitor_adder():
    return get_adder('nama pengguna', fname=users_file)


def blacklist_adder():
    return get_adder('nama pengguna', fname=blacklist)


def whitelist_adder():
    return get_adder('nama pengguna', fname=whitelist)


def comment_adder():
    return get_adder('comment', fname=comment)


def userlist_maker():
    return get_adder('nama pengguna', userlist)


# all menu start here

def menu():
    ans = True
    while ans:
        print("""
        1.Follow
        2.Like
        3.Comment
        4.Unfollow
        5.Block
        6.Setting
        7.Exit
        """)
        ans = input("Pilih Salah Satu Buat Meretas\n").strip()
        if ans == "1":
            menu_follow()
        elif ans == "2":
            menu_like()
        elif ans == "3":
            menu_comment()
        elif ans == "4":
            menu_unfollow()
        elif ans == "5":
            menu_block()
        elif ans == "6":
            menu_setting()
        elif ans == "7":
            bot.logout()
            sys.exit()
        else:
            print("\n Bukan Pilihan yang Valid, Coba lagi")


def menu_follow():
    ans = True
    while ans:
        print("""
        1. Follow from hashtag
        2. Follow followers
        3. Follow following
        4. Follow by likes on media
        5. Main menu
        """)
        ans = input("Bagaimana Anda ingin mengikuti?\n").strip()

        if ans == "1":
            print("""
            1.Masukkan tagar
            2.Gunakan basis data hashtag
            """)
            hashtags = []
            if "1" in sys.stdin.readline():
                hashtags = input("Insert hashtags separated by spaces\nExample: cat dog\nwhat hashtags?\n").strip().split(' ')
            else:
                hashtags = bot.read_list_from_file(hashtag_file)
            for hashtag in hashtags:
                print("Mulai ikuti: " + hashtag)
                users = bot.get_hashtag_users(hashtag)
                bot.follow_users(users)
            menu_follow()

        elif ans == "2":
            print("""
            1.Masukkan nama pengguna
            2.Gunakan basis data nama pengguna
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_followers(user_id)
            menu_follow()

        elif ans == "3":
            print("""
            1.Masukkan nama pengguna
            2.Gunakan basis data nama pengguna
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_following(user_id)
            menu_follow()

        elif ans == "4":
            print("""
            1.Masukkan nama pengguna
            2.Gunakan basis data nama pengguna
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            medias = bot.get_user_medias(user_id, filtration=False)
            if len(medias):
                likers = bot.get_media_likers(medias[0])
                for liker in tqdm(likers):
                    bot.follow(liker)

        elif ans == "5":
            menu()

        else:
            print("Nomor ini tidak ada dalam daftar")
            menu_follow()


def menu_like():
    ans = True
    while ans:
        print("""
        1. Like from hashtag(s)
        2. Like followers
        3. Like following
        4. Like last media likers
        5. Like our timeline
        6. Main menu
        """)
        ans = input("Anda ingin seperti apa?\n").strip()

        if ans == "1":
            print("""
            1.Masukkan tagar
            2.Gunakan basis data hashtag
            """)
            hashtags = []
            if "1" in sys.stdin.readline():
                hashtags = input("Insert hashtags separated by spaces\nExample: cat dog\nwhat hashtags?\n").strip().split(' ')
            else:
                hashtags.append(random.choice(bot.read_list_from_file(hashtag_file)))
            for hashtag in hashtags:
                bot.like_hashtag(hashtag)

        elif ans == "2":
            print("""
            1.Masukkan nama pengguna
            2.Gunakan basis data nama pengguna
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.like_followers(user_id)

        elif ans == "3":
            print("""
            1.Masukkan nama pengguna
            2.Gunakan basis data nama pengguna
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.like_following(user_id)

        elif ans == "4":
            print("""
            1.Masukkan nama pengguna
            2.Gunakan basis data nama pengguna
            """)
            if "1" in sys.stdin.readline():
                user_id = input("SIAPA?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            medias = bot.get_user_medias(user_id, filtration=False)
            if len(medias):
                likers = bot.get_media_likers(medias[0])
                for liker in tqdm(likers):
                    bot.like_user(liker, amount=2, filtration=False)

        elif ans == "5":
            bot.like_timeline()

        elif ans == "6":
            menu()

        else:
            print("Nomor ini tidak ada dalam daftar?")
            menu_like()


def menu_comment():
    ans = True
    while ans:
        print("""
        1. Comment from hashtag
        2. Comment spesific user media
        3. Comment userlist
        4. Comment our timeline
        5. Main menu
        """)
        ans = input("How do you want to comment?\n").strip()

        if ans == "1":
            print("""
            1.Masukkan tagar
            2.Gunakan basis data hashtag
            """)
            if "1" in sys.stdin.readline():
                hashtag = input("AdaApa?").strip()
            else:
                hashtag = random.choice(bot.read_list_from_file(hashtag_file))
            bot.comment_hashtag(hashtag)

        elif ans == "2":
            print("""
            1.Masukkan nama pengguna
            2.Gunakan basis data nama pengguna
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.comment_medias(bot.get_user_medias(user_id, filtration=False))

        elif ans == "3":
            print("""
            1. Buat daftar
            2.Gunakan daftar yang ada
            """)
            if "1" in sys.stdin.readline():
                userlist_maker()
            if "2" in sys.stdin.readline():
                print(userlist)
            users = bot.read_list_from_file(userlist)
            for user_id in users:
                bot.comment_medias(
                    bot.get_user_medias(
                        user_id, filtration=True))

        elif ans == "4":
            bot.comment_medias(bot.get_timeline_medias())

        elif ans == "5":
            menu()

        else:
            print("Anda Salah Masukan Nomor")
            menu_comment()


def menu_unfollow():
    ans = True
    while ans:
        print("""
        1. Unfollow non followers
        2. Unfollow everyone
        3. Main menu
        """)
        ans = input("Pilih Salah Satu Buat Unfollow?\n").strip()

        if ans == "1":
            bot.unfollow_non_followers()
            menu_unfollow()

        elif ans == "2":
            bot.unfollow_everyone()
            menu_unfollow()

        elif ans == "3":
            menu()

        else:
            print("Nomor Ini Tidak Terdaftar")
            menu_unfollow()


def menu_block():
    ans = True
    while ans:
        print("""
        1. Block bot
        2. Main menu
        """)
        ans = input("Pilih Salah Satu Untuk block?\n").strip()
        if ans == "1":
            bot.block_bots()
            menu_block()

        elif ans == "2":
            menu()

        else:
            print("Nomor Tidak Terdaftar Eroor NUll")
            menu_block()


def menu_setting():
    ans = True
    while ans:
        print("""
         1. Pengaturan parameter bot
         2. Tambahkan akun pengguna
         3. Tambahkan basis data pesaing
         4. Tambahkan basis data hashtag
         5. Tambahkan basis data Komentar
         6. Tambahkan daftar hitam
         7. Tambahkan daftar putih
         8. Bersihkan semua basis data
         9. Menu utama
        """)
        ans = input("Apa Yang Anda Lakukan Di Pengaturan?\n").strip()

        if ans == "1":
            parameter_setting()
            change = input("Apakah Anda Ingin Menganti? y/n\n").strip()
            if change == 'y' or change == 'Y':
                setting_input()
            else:
                menu_setting()
        elif ans == "2":
            username_adder()
        elif ans == "3":
            competitor_adder()
        elif ans == "4":
            hashtag_adder()
        elif ans == "5":
            comment_adder()
        elif ans == "6":
            blacklist_adder()
        elif ans == "7":
            whitelist_adder()
        elif ans == "8":
            print(
                "Ini akan menghapus semua basis data kecuali akun pengguna dan pengaturan parameter Anda")
            time.sleep(5)
            open(hashtag_file, 'w')
            open(users_file, 'w')
            open(whitelist, 'w')
            open(blacklist, 'w')
            open(comment, 'w')
            print("Done, Kamu Bisa Menambah Satu Lagi")
        elif ans == "9":
            menu()
        else:
            print("Eror FAILED)
            menu_setting()


# for input compability
try:
    input = raw_input
except NameError:
    pass

# files location
hashtag_file = "hashtagsdb.txt"
users_file = "usersdb.txt"
whitelist = "whitelist.txt"
blacklist = "blacklist.txt"
userlist = "userlist.txt"
comment = "comment.txt"
setting = "setting.txt"
SECRET_FILE = "secret.txt"

# check setting first
initial_checker()

if os.stat(setting).st_size == 0:
    print("Looks like setting are broken")
    print("Let's make new one")
    setting_input()

f = open(setting)
lines = f.readlines()
setting_0 = int(lines[0].strip())
setting_1 = int(lines[1].strip())
setting_2 = int(lines[2].strip())
setting_3 = int(lines[3].strip())
setting_4 = int(lines[4].strip())
setting_5 = int(lines[5].strip())
setting_6 = int(lines[6].strip())
setting_7 = int(lines[7].strip())
setting_8 = int(lines[8].strip())
setting_9 = int(lines[9].strip())
setting_10 = int(lines[10].strip())
setting_11 = int(lines[11].strip())
setting_12 = int(lines[12].strip())
setting_13 = int(lines[13].strip())
setting_14 = int(lines[14].strip())
setting_15 = int(lines[15].strip())
setting_16 = int(lines[16].strip())
setting_17 = int(lines[17].strip())
setting_18 = lines[18].strip()

bot = Bot(
    max_likes_per_day=setting_0,
    max_unlikes_per_day=setting_1,
    max_follows_per_day=setting_2,
    max_unfollows_per_day=setting_3,
    max_comments_per_day=setting_4,
    max_likes_to_like=setting_5,
    max_followers_to_follow=setting_6,
    min_followers_to_follow=setting_7,
    max_following_to_follow=setting_8,
    min_following_to_follow=setting_9,
    max_followers_to_following_ratio=setting_10,
    max_following_to_followers_ratio=setting_11,
    min_media_count_to_follow=setting_12,
    like_delay=setting_13,
    unlike_delay=setting_14,
    follow_delay=setting_15,
    unfollow_delay=setting_16,
    comment_delay=setting_17,
    whitelist_file=whitelist,
    blacklist_file=blacklist,
    comments_file=comment,
    stop_words=[
        'order',
        'shop',
        'store',
        'free',
        'doodleartindonesia',
        'doodle art indonesia',
        'fullofdoodleart',
        'commission',
        'vector',
        'karikatur',
        'jasa',
        'open'])

bot.login()

while True:
    try:
        menu()
    except Exception as e:
        bot.logger.info("error, read exception bellow")
        bot.logger.info(str(e))
    time.sleep(1)
