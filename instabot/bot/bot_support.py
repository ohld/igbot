"""
    Support instabot's methods.
"""

from __future__ import unicode_literals

import codecs
import os
import re
import sys

import huepy


def check_if_file_exists(file_path, quiet=False):
    if not os.path.exists(file_path):
        if not quiet:
            print("Can't find '%s' file." % file_path)
        return False
    return True


def read_list_from_file(file_path, quiet=False):
    """
        Reads list from file. One line - one item.
        Returns the list if file items.
    """
    try:
        if not check_if_file_exists(file_path, quiet=quiet):
            return []
        with codecs.open(file_path, "r", encoding="utf-8") as f:
            content = f.readlines()
            if sys.version_info[0] < 3:
                content = [str(item.encode("utf8")) for item in content]
            content = [item.strip() for item in content]
            return [i for i in content if i]
    except Exception as exception:
        print(str(exception))
        return []


def console_print(self, text, color=None):
    if self.verbosity:
        text = "\n" + text
        if color is not None:
            text = getattr(huepy, color)(text)
        print(text)


def extract_urls(text):
    url_regex = (
        r"((?:(?:http|https|Http|Https|rtsp|Rtsp)://"
        r"(?:(?:[a-zA-Z0-9$\-\_\.\+\!\*\'\(\)\,\;\?\&\=]|(?:%[a-fA-F0-9]"
        r"{2})){1,64}(?::(?:[a-zA-Z0-9$\-\_\.\+\!\*\'\(\)\,\;\?\&\=]|"
        r"(?:%[a-fA-F0-9]{2})){1,25})?@)?)?(?:(?:(?:[a-zA-Z0-9"
        r"\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF\_][a-zA-Z0-9"
        r"\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF\_\-]{0,64}\.)+(?:(?:aero|"
        r"arpa|asia|a[cdefgilmnoqrstuwxz])|(?:biz|b[abdefghijmnorstvwyz])|"
        r"(?:cat|com|coop|c[acdfghiklmnoruvxyz])|d[ejkmoz]|(?:edu|e[cegrstu])"
        r"|f[ijkmor]|(?:gov|g[abdefghilmnpqrstuwy])|h[kmnrtu]|(?:info|int|i"
        r"[delmnoqrst])|(?:jobs|j[emop])|k[eghimnprwyz]|l[abcikrstuvy]|(?:mil"
        r"|mobi|museum|m[acdeghklmnopqrstuvwxyz])|(?:name|net|n[acefgilopruz])"
        r"|(?:org|om)|(?:pro|p[aefghklmnrstwy])|qa|r[eosuw]|s[abcdeghijklmnort"
        r"uvyz]|(?:tel|travel|t[cdfghjklmnoprtvwz])|u[agksyz]|v[aceginu]"
        r"|w[fs]|(?:\u03B4\u03BF\u03BA\u03B9\u03BC\u03AE|"
        r"\u0438\u0441\u043F\u044B\u0442\u0430\u043D\u0438\u0435|\u0440\u0444|"
        r"\u0441\u0440\u0431|\u05D8\u05E2\u05E1\u05D8|"
        r"\u0622\u0632\u0645\u0627\u06CC\u0634\u06CC|"
        r"\u0625\u062E\u062A\u0628\u0627\u0631|\u0627\u0644\u0627\u0631\u062F"
        r"\u0646|\u0627\u0644\u062C\u0632\u0627\u0626\u0631|"
        r"\u0627\u0644\u0633\u0639\u0648\u062F\u064A\u0629|"
        r"\u0627\u0644\u0645\u063A\u0631\u0628|\u0627\u0645\u0627\u0631\u0627"
        r"\u062A|\u0628\u06BE\u0627\u0631\u062A|\u062A\u0648\u0646\u0633|"
        r"\u0633\u0648\u0631\u064A\u0629|\u0641\u0644\u0633\u0637\u064A\u0646|"
        r"\u0642\u0637\u0631|\u0645\u0635\u0631|"
        r"\u092A\u0930\u0940\u0915\u094D\u0937\u093E|\u092D\u093E\u0930\u0924|"
        r"\u09AD\u09BE\u09B0\u09A4|\u0A2D\u0A3E\u0A30\u0A24|"
        r"\u0AAD\u0ABE\u0AB0\u0AA4|\u0B87\u0BA8\u0BCD\u0BA4\u0BBF\u0BAF\u0BBE|"
        r"\u0B87\u0BB2\u0B99\u0BCD\u0B95\u0BC8|"
        r"\u0B9A\u0BBF\u0B99\u0BCD\u0B95\u0BAA\u0BCD\u0BAA\u0BC2\u0BB0\u0BCD|"
        r"\u0BAA\u0BB0\u0BBF\u0B9F\u0BCD\u0B9A\u0BC8|\u0C2D\u0C3E\u0C30\u0C24"
        r"\u0C4D|\u0DBD\u0D82\u0D9A\u0DCF|\u0E44\u0E17\u0E22|\u30C6\u30B9"
        r"\u30C8|\u4E2D\u56FD|\u4E2D\u570B|\u53F0\u6E7E|\u53F0\u7063|\u65B0"
        r"\u52A0\u5761|\u6D4B\u8BD5|\u6E2C\u8A66|\u9999\u6E2F|\uD14C\uC2A4"
        r"\uD2B8|\uD55C\uAD6D|xn--0zwm56d|xn--11b5bs3a9aj6g|xn--3e0b707e"
        r"|xn--45brj9c|xn--80akhbyknj4f|xn--90a3ac|xn--9t4b11yi5a|xn--clchc0ea"
        r"0b2g2a9gcd|xn--deba0ad|xn--fiqs8s|xn--fiqz9s|xn--fpcrj9c3d|xn--"
        r"fzc2c9e2c|xn--g6w251d|xn--gecrj9c|xn--h2brj9c|xn--hgbk6aj7f53bba|xn"
        r"--hlcj6aya9esc7a|xn--j6w193g|xn--jxalpdlp|xn--kgbechtv|xn--kprw13d|"
        r"xn--kpry57d|xn--lgbbat1ad8j|xn--mgbaam7a8h|xn--mgbayh7gpa|"
        r"xn--mgbbh1a71e|xn--mgbc0a9azcg|xn--mgberp4a5d4ar|xn--o3cw4h|"
        r"xn--ogbpf8fl|xn--p1ai|xn--pgbs0dh|xn--s9brj9c|xn--wgbh1c|xn--wgbl6a|"
        r"xn--xkc2al3hye2a|xn--xkc2dl3a5ee0h|xn--yfro4i67o|xn--ygbi2ammx|"
        r"xn--zckzah|xxx)|y[et]|z[amw]))|(?:(?:25[0-5]|2[0-4][0-9]|"
        r"[0-1][0-9]{2}|[1-9][0-9]|[1-9])\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]"
        r"{2}|[1-9][0-9]|[1-9]|0)\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9]"
        r"[0-9]|[1-9]|0)\.(?:25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|"
        r"[0-9])))(?::\d{1,5})?(?:/(?:(?:[a-zA-Z0-9\u00A0-\uD7FF\uF900-\uFDCF"
        r"\uFDF0-\uFFEF\;\/\?\:\@\&\=\#\~\-\.\+\!\*\'\(\)\,\_])|"
        r"(?:%[a-fA-F0-9]{2}))*)?)(?:\b|$)"
    )  # noqa
    urls = re.findall(url_regex, text)

    return urls
