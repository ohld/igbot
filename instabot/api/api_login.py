import json
import os
import random
import time
import traceback

import requests
import requests.utils

from . import config, devices

# ====== SYNC METHODS ====== #


def sync_device_features(self, login=False):
    data = {
        "id": self.uuid,
        "server_config_retrieval": "1",
        "experiments": config.LOGIN_EXPERIMENTS,
    }
    if login is False:
        data["_uuid"] = self.uuid
        data["_uid"] = self.user_id
        data["_csrftoken"] = self.token
    data = json.dumps(data)
    return self.send_request(
        "qe/sync/", data, login=login, headers={"X-DEVICE-ID": self.uuid}
    )


def sync_launcher(self, login=False):
    data = {
        "id": self.uuid,
        "server_config_retrieval": "1",
        "experiments": config.LAUNCHER_CONFIGS,
    }
    if login is False:
        data["_uuid"] = self.uuid
        data["_uid"] = self.user_id
        data["_csrftoken"] = self.token
    data = json.dumps(data)
    return self.send_request("launcher/sync/", data, login=login)


def sync_user_features(self):
    data = self.default_data
    data["id"] = self.uuid
    data["experiments"] = config.EXPERIMENTS
    data = json.dumps(data)
    self.last_experiments = time.time()
    return self.send_request(
        "qe/sync/",
        data,
        headers={"X-DEVICE-ID": self.uuid}
    )


# ====== LOGIN/PRE FLOWS METHODS ====== #


def pre_login_flow(self):
    self.logger.info("PRE-LOGIN FLOW!... ")

    self.read_msisdn_header("default")
    self.sync_launcher(True)
    self.sync_device_features(True)
    self.log_attribution()
    self.set_contact_point_prefill("prefill")


def login_flow(self, just_logged_in=False, app_refresh_interval=1800):
    self.logger.info("LOGIN FLOW! Just logged-in: {}".format(just_logged_in))
    check_flow = []
    if just_logged_in:
        try:
            # SYNC
            check_flow.append(self.sync_launcher(False))
            check_flow.append(self.sync_user_features())
            # Update feed and timeline
            check_flow.append(self.get_timeline_feed())
            check_flow.append(self.get_reels_tray_feed(reason="cold_start"))
            check_flow.append(self.get_suggested_searches("users"))
            # getRecentSearches() ...
            check_flow.append(self.get_suggested_searches("blended"))
            # DM-Update
            check_flow.append(self.get_ranked_recipients("reshare", True))
            check_flow.append(self.get_ranked_recipients("save", True))
            check_flow.append(self.get_inbox_v2())
            check_flow.append(self.get_presence())
            check_flow.append(self.get_recent_activity())
            # Config and other stuffs
            check_flow.append(self.get_loom_fetch_config())
            check_flow.append(self.get_profile_notice())
            check_flow.append(self.batch_fetch())
            # getBlockedMedia() ...
            check_flow.append(self.explore(True))
            # getQPFetch() ...
            # getFacebookOTA() ...
        except Exception as e:
            self.logger.error(
                "Exception raised: {}\n{}".format(e, traceback.format_exc())
            )
            return False
    else:
        try:
            pull_to_refresh = random.randint(1, 100) % 2 == 0
            check_flow.append(
                self.get_timeline_feed(
                    options=["is_pull_to_refresh"]
                    if pull_to_refresh is True else []
                )
            )  # Random pull_to_refresh :)
            check_flow.append(
                self.get_reels_tray_feed(
                    reason="pull_to_refresh"
                    if pull_to_refresh is True
                    else "cold_start"
                )
            )

            is_session_expired = \
                (time.time() - self.last_login) > app_refresh_interval
            if is_session_expired:
                self.last_login = time.time()
                self.client_session_id = self.generate_UUID(uuid_type=True)

                # getBootstrapUsers() ...
                check_flow.append(self.get_ranked_recipients("reshare", True))
                check_flow.append(self.get_ranked_recipients("save", True))
                check_flow.append(self.get_inbox_v2())
                check_flow.append(self.get_presence())
                check_flow.append(self.get_recent_activity())
                check_flow.append(self.get_profile_notice())
                check_flow.append(self.explore(False))

            if (time.time() - self.last_experiments) > 7200:
                check_flow.append(self.sync_user_features())
                check_flow.append(self.sync_device_features())
        except Exception as e:
            self.logger.error(
                "Exception raised: {}\n{}".format(e, traceback.format_exc())
            )
            return False

    self.save_uuid_and_cookie()
    return False if False in check_flow else True


# ====== DEVICE / CLIENT_ID / PHONE_ID AND OTHER VALUES (uuids) ====== #


def set_device(self):
    self.device_settings = devices.DEVICES[self.device]
    self.user_agent = config.USER_AGENT_BASE.format(**self.device_settings)


def generate_all_uuids(self):
    self.phone_id = self.generate_UUID(uuid_type=True)
    self.uuid = self.generate_UUID(uuid_type=True)
    self.client_session_id = self.generate_UUID(uuid_type=True)
    self.advertising_id = self.generate_UUID(uuid_type=True)
    self.device_id = self.generate_device_id(
        self.get_seed(self.username, self.password)
    )


def reinstall_app_simulation(self):
    self.logger.info("Reinstall app simulation, generating new `phone_id`...")
    self.phone_id = self.generate_UUID(uuid_type=True)
    self.save_uuid_and_cookie()
    self.logger.info("New phone_id: {}".format(self.phone_id))


def change_device_simulation(self):
    self.logger.info("Change device simulation")
    self.reinstall_app_simulation()
    self.logger.info("Generating new `android_device_id`...")
    self.device_id = self.generate_device_id(
        self.get_seed(self.generate_UUID(uuid_type=True))
    )
    self.save_uuid_and_cookie()
    self.logger.info("New android_device_id: {}".format(self.device_id))


def load_uuid_and_cookie(self, load_uuid=True, load_cookie=True):
    if self.cookie_fname is None:
        fname = "{}_uuid_and_cookie.json".format(self.username)
        self.cookie_fname = os.path.join(self.base_path, fname)

    if os.path.isfile(self.cookie_fname) is False:
        return False

    with open(self.cookie_fname, "r") as f:
        data = json.load(f)
        if "cookie" in data:
            self.last_login = data["timing_value"]["last_login"]
            self.last_experiments = data["timing_value"]["last_experiments"]

            if load_cookie:
                self.logger.debug("Loading cookies")
                self.session.cookies = requests.utils.cookiejar_from_dict(
                    data["cookie"]
                )
                cookie_username = self.cookie_dict["ds_user"]
                assert cookie_username == self.username.lower()

            if load_uuid:
                self.logger.debug("Loading uuids")
                self.phone_id = data["uuids"]["phone_id"]
                self.uuid = data["uuids"]["uuid"]
                self.client_session_id = data["uuids"]["client_session_id"]
                self.advertising_id = data["uuids"]["advertising_id"]
                self.device_id = data["uuids"]["device_id"]

                self.device_settings = data["device_settings"]
                self.user_agent = data["user_agent"]

            msg = ("Recovery from {}: COOKIE {} - UUIDs {} - TIMING, DEVICE "
                   "and ...\n- user-agent={}\n- phone_id={}\n- uuid={}\n- "
                   "client_session_id={}\n- device_id={}")

            self.logger.info(msg.format(
                self.cookie_fname,
                load_cookie,
                load_uuid,
                self.user_agent,
                self.phone_id,
                self.uuid,
                self.client_session_id,
                self.device_id,
                )
            )
        else:
            self.logger.info(
                "The cookie seems to be the with the older structure. "
                "Load and init again all uuids"
            )
            self.session.cookies = requests.utils.cookiejar_from_dict(data)
            self.last_login = time.time()
            self.last_experiments = time.time()
            cookie_username = self.cookie_dict["ds_user"]
            assert cookie_username == self.username
            self.set_device()
            self.generate_all_uuids()

    self.is_logged_in = True
    return True


def save_uuid_and_cookie(self):
    if self.cookie_fname is None:
        fname = "{}_uuid_and_cookie.json".format(self.username)
        self.cookie_fname = os.path.join(self.base_path, fname)

    data = {
        "uuids": {
            "phone_id": self.phone_id,
            "uuid": self.uuid,
            "client_session_id": self.client_session_id,
            "advertising_id": self.advertising_id,
            "device_id": self.device_id,
        },
        "cookie": requests.utils.dict_from_cookiejar(self.session.cookies),
        "timing_value": {
            "last_login": self.last_login,
            "last_experiments": self.last_experiments,
        },
        "device_settings": self.device_settings,
        "user_agent": self.user_agent,
    }
    with open(self.cookie_fname, "w") as f:
        json.dump(data, f)
