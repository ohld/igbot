# flake8: noqa
# Devices taken from:
# https://github.com/mgp25/Instagram-API/blob/
#   master/src/Devices/GoodDevices.php
DEFAULT_DEVICE = "one_plus_7"
# from https://www.apkmirror.com/apk/instagram/instagram-instagram/
#   instagram-instagram-105-0-0-18-119-release/instagram-105-0-0-18
#   -119-4-android-apk-download/
INSTAGRAM_VERSION = "105.0.0.18.119"
DEVICES = {
    # Released on August 2019
    "one_plus_7": {
        "instagram_version": INSTAGRAM_VERSION,
        "android_version": 28,
        "android_release": "9.0",
        "dpi": "420dpi",
        "resolution": "1080x2260",
        "manufacturer": "OnePlus",
        "device": "GM1903",
        "model": "OnePlus7",
        "cpu": "qcom",
    },
    # Released on March 2016
    "samsung_galaxy_s7": {
        "instagram_version": INSTAGRAM_VERSION,
        "android_version": 24,
        "android_release": "7.0",
        "dpi": "640dpi",
        "resolution": "1440x2560",
        "manufacturer": "samsung",
        "device": "SM-G930F",
        "model": "herolte",
        "cpu": "samsungexynos8890",
    },
    # Released on January 2017
    "huawei_mate_9_pro": {
        "instagram_version": INSTAGRAM_VERSION,
        "android_version": 24,
        "android_release": "7.0",
        "dpi": "640dpi",
        "resolution": "1440x2560",
        "manufacturer": "HUAWEI",
        "device": "LON-L29",
        "model": "HWLON",
        "cpu": "hi3660",
    },
    # Released on February 2018
    "samsung_galaxy_s9_plus": {
        "instagram_version": INSTAGRAM_VERSION,
        "android_version": 24,
        "android_release": "7.0",
        "dpi": "640dpi",
        "resolution": "1440x2560",
        "manufacturer": "samsung",
        "device": "SM-G965F",
        "model": "star2qltecs",
        "cpu": "samsungexynos9810",
    },
    # Released on November 2016
    "one_plus_3t": {
        "instagram_version": INSTAGRAM_VERSION,
        "android_version": 24,
        "android_release": "7.0",
        "dpi": "380dpi",
        "resolution": "1080x1920",
        "manufacturer": "OnePlus",
        "device": "ONEPLUS A3010",
        "model": "OnePlus3T",
        "cpu": "qcom",
    },
    # Released on April 2016
    "lg_g5": {
        "instagram_version": INSTAGRAM_VERSION,
        "android_version": 23,
        "android_release": "6.0.1",
        "dpi": "640dpi",
        "resolution": "1440x2392",
        "manufacturer": "LGE/lge",
        "device": "RS988",
        "model": "h1",
        "cpu": "h1",
    },
    # Released on June 2016
    "zte_axon_7": {
        "instagram_version": INSTAGRAM_VERSION,
        "android_version": 23,
        "android_release": "6.0.1",
        "dpi": "640dpi",
        "resolution": "1440x2560",
        "manufacturer": "ZTE",
        "device": "ZTE A2017U",
        "model": "ailsa_ii",
        "cpu": "qcom",
    },
    # Released on March 2016
    "samsung_galaxy_s7_edge": {
        "instagram_version": INSTAGRAM_VERSION,
        "android_version": 23,
        "android_release": "6.0.1",
        "dpi": "640dpi",
        "resolution": "1440x2560",
        "manufacturer": "samsung",
        "device": "SM-G935",
        "model": "hero2lte",
        "cpu": "samsungexynos8890",
    },
}
