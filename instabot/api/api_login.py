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
    self.last_experiments = time.time()
    return self.send_request(
        "qe/sync/", data, login=login, headers={"X-DEVICE-ID": self.uuid}
    )


def sync_launcher(self, login=False):
    data = {
        "id": self.uuid,
        "server_config_retrieval": "1",
    }
    if login is False:
        data["_uid"] = self.user_id
        data["_uuid"] = self.uuid
        data["_csrftoken"] = self.token
    data = json.dumps(data)
    return self.send_request("launcher/sync/", data, login=login)


def sync_user_features(self):
    data = self.default_data
    data["id"] = self.uuid
    data["experiments"] = config.EXPERIMENTS
    data = json.dumps(data)
    self.last_experiments = time.time()
    return self.send_request("qe/sync/", data, headers={"X-DEVICE-ID": self.uuid})


# "android_device_id":"android-f14b9731e4869eb",
# "phone_id":"b4bd7978-ca2b-4ea0-a728-deb4180bd6ca",
# "usages":"[\"account_recovery_omnibox\"]",
# "_csrftoken":"9LZXBXXOztxNmg3h1r4gNzX5ohoOeBkI",
# "device_id":"70db6a72-2663-48da-96f5-123edff1d458"
def get_prefill_candidates(self, login=False):
    data = {
        "android_device_id": self.device_id,
        "phone_id": self.phone_id,
        "usages": '["account_recovery_omnibox"]',
        "device_id": self.device_id,
    }
    if login is False:
        data["_csrftoken"] = self.token
    data = json.dumps(data)
    return self.send_request("accounts/get_prefill_candidates/", data, login=login)


def get_account_family(self):
    return self.send_request("multiple_accounts/get_account_family/")


def get_zr_token_result(self):
    url = (
        "zr/token/result/?device_id={rank_token}"
        "&token_hash=&custom_device_id={custom_device_id}&fetch_reason=token_expired"
    )
    url = url.format(rank_token=self.device_id, custom_device_id=self.device_id)
    return self.send_request(url)


def banyan(self):
    url = "banyan/banyan/?views=['story_share_sheet','threads_people_picker','group_stories_share_sheet','reshare_share_sheet']"
    return self.send_request(url)


def igtv_browse_feed(self):
    url = "igtv/browse_feed/?prefetch=1"
    return self.send_request(url)


def creatives_ar_class(self):
    data = {
        "_csrftoken": self.token,
        "_uuid": self.uuid,
    }
    data = json.dumps(data)
    return self.send_request("creatives/ar_class/", data)


# ====== LOGIN/PRE FLOWS METHODS ====== #


def pre_login_flow(self):
    self.logger.info("Not yet logged in starting: PRE-LOGIN FLOW!")

    # /api/v1/accounts/get_prefill_candidates
    self.get_prefill_candidates(True)

    # /api/v1/qe/sync (server_config_retrieval)
    self.sync_device_features(True)

    # /api/v1/launcher/sync/ (server_config_retrieval)
    self.sync_launcher(True)

    # /api/v1/accounts/contact_point_prefill/
    self.set_contact_point_prefill("prefill")

    # /api/v1/accounts/get_prefill_candidates/
    # self.get_prefill_candidates(True)

    # /api/v1/accounts/contact_point_prefill/
    # self.set_contact_point_prefill("prefill")

    # /api/v1/qe/sync/ (server_config_retrieval)
    # self.sync_device_features(True)

    # /api/v1/launcher/sync/ (server_config_retrieval)
    # self.sync_launcher(True)


# DO NOT MOVE ANY OF THE ENDPOINTS THEYRE IN THE CORRECT ORDER
def login_flow(self, just_logged_in=False, app_refresh_interval=1800):
    self.last_experiments = time.time()
    self.logger.info("LOGIN FLOW! Just logged-in: {}".format(just_logged_in))
    check_flow = []
    if just_logged_in:
        try:
            # SYNC
            # /api/v1/qe/sync/ (server_config_retrieval)
            check_flow.append(self.sync_device_features())

            # /api/v1/launcher/sync/ (server_config_retrieval)
            check_flow.append(self.sync_launcher(False))

            # /api/v1/zr/token/result/?device_id=android-f14b9731e4869eb&token_hash=&custom_device_id=f3119c98-5663-4c47-95b5-a63b140a2b62&fetch_reason=token_expired
            check_flow.append(self.get_zr_token_result())

            # /api/v1/multiple_accounts/get_account_family/
            check_flow.append(self.get_account_family())

            # /api/v1/qe/sync/ (server_config_retrieval)
            check_flow.append(self.sync_device_features())

            # /api/v1/banyan/banyan/?views=%5B%22story_share_sheet%22%2C%22threads_people_picker%22%2C%22group_stories_share_sheet%22%2C%22reshare_share_sheet%22%5D
            # error 400: {"message": "Bad request", "status": "fail"}
            # check_flow.append(self.banyan())

            # /api/v1/igtv/browse_feed/?prefetch=1
            check_flow.append(self.igtv_browse_feed())

            # /api/v1/creatives/ar_class/ (_csrftoken also add _uuid)
            check_flow.append(self.creatives_ar_class())

            # /api/v1/feed/reels_tray/ (supported_capabilities_new + reason=cold_start + _csrftoken + _uuid)
            check_flow.append(self.get_reels_tray_feed(reason="cold_start"))

            # /api/v1/feed/timeline/ (feed_view_info + phone_id + battery_level + timezone_offset + _csrftoken + device_id + request_id + is_pull_to_refresh=0 + _uuid + is_charging=1 + will_sound_on=0 + seesion_id + bloks_versioning_id)
            check_flow.append(self.get_timeline_feed())

            # /api/v1/feed/reels_media/
            # error 400: {"message": "Invalid reel id list", "status": "fail"}
            # check_flow.append(self.get_reels_media())

            # /api/v1/push/register/ (device_type=android_mqtt + is_main_push_channel=true + device_sub_type=2 + device_toke + _csrftoken + guid + _uuid + users + family_device_id)
            # device_type=android_mqtt&is_main_push_channel=true&device_sub_type=2&device_token={"k":"eyJwbiI6ImNvbS5pbnN0YWdyYW0uYW5kcm9pZCIsImRpIjoiNzhlNGMxNmQtN2YzNC00NDlkLTg4OWMtMTAwZDg5OTU0NDJhIiwiYWkiOjU2NzMxMDIwMzQxNTA1MiwiY2siOiIxNjgzNTY3Mzg0NjQyOTQifQ==","v":0,"t":"fbns-b64"}&_csrftoken=mmdoMLXFQEzt2w5xLbfm0FTs7gIgqAlc&guid=f87b5e9f-0663-42f8-9213-ec72cb49c961&_uuid=f87b5e9f-0663-42f8-9213-ec72cb49c961&users=3149016955&family_device_id=9d9aa0f0-40fe-4524-a920-9910f45ba18d
            # error 400: {"message": "no token provided", "status": "fail"}
            # check_flow.append(self.push_register())

            # /api/v1/feed/reels_media/
            # error 400: {"message": "Invalid reel id list", "status": "fail"}
            # check_flow.append(self.get_reels_media())

            # /api/v1/media/blocked/
            check_flow.append(self.media_blocked())

            # /api/v1/news/inbox/
            check_flow.append(self.get_news_inbox())

            # /api/v1/loom/fetch_config/
            check_flow.append(self.get_loom_fetch_config())

            # /api/v1/scores/bootstrap/users/?surfaces=%5B%22autocomplete_user_list%22%2C%22coefficient_besties_list_ranking%22%2C%22coefficient_rank_recipient_user_suggestion%22%2C%22coefficient_ios_section_test_bootstrap_ranking%22%2C%22coefficient_direct_recipients_ranking_variant_2%22%5D
            check_flow.append(self.get_scores_bootstrap())

            # /api/v1/business/eligibility/get_monetization_products_eligibility_data/?product_types=branded_content
            check_flow.append(self.get_monetization_products_eligibility_data())

            # /api/v1/business/branded_content/should_require_professional_account/
            check_flow.append(self.get_business_branded_content())

            # /api/v1/linked_accounts/get_linkage_status/
            check_flow.append(self.get_linked_accounts())

            # /api/v1/locations/request_country/
            check_flow.append(self.get_request_country())

            # /api/v1/qp/get_cooldowns/?signed_body=a7c6081ee2ae5b41a1475f83b6dbc8f1130c67d472f69748221468e1621823b5.%7B%7D&ig_sig_key_version=4
            check_flow.append(self.get_cooldowns())

            # /api/v1/users/arlink_download_info/?version_override=2.2.1
            check_flow.append(self.arlink_download_info())

            # push register
            # error 400: {"message": "no token provided", "status": "fail"}
            # check_flow.append(self.push_register())

            # /api/v1/users/self.user_id/info/
            check_flow.append(self.get_username_info(self.user_id))

            # /api/v1/notifications/store_client_push_permissions/
            # error 400: {"message": "missing param", "status": "fail"}
            # check_flow.append(self.log_resurrect_attribution())

            # /api/v1/accounts/process_contact_point_signals
            # error 400: {"message": "", "status": "fail"}
            # check_flow.append(self.process_contact_point_signals())

            # creatives/write_supported_capabilities
            # error 500: unknown
            # check_flow.append(self.write_supported_capabilities())

            check_flow.append(self.get_presence())
            check_flow.append(self.get_direct_v2_inbox())
            check_flow.append(self.get_direct_v2_inbox2())
            check_flow.append(self.topical_explore())
            check_flow.append(self.notification_badge())
            check_flow.append(self.batch_fetch())

            # TODO add facebook_ota
            # /api/v1/facebook_ota/?fields=update%7Bdownload_uri%2Cdownload_uri_delta_base%2Cversion_code_delta_base%2Cdownload_uri_delta%2Cfallback_to_full_update%2Cfile_size_delta%2Cversion_code%2Cpublished_date%2Cfile_size%2Cota_bundle_type%2Cresources_checksum%2Callowed_networks%2Crelease_id%7D&custom_user_id=3149016955&signed_body=656adcfd879d775324e9c1668534f80a999801c7780f16cc720d7970941195de.&ig_sig_key_version=4&version_code=195435566&version_name=126.0.0.25.121&custom_app_id=124024574287414&custom_device_id=f87b5e9f-0663-42f8-9213-ec72cb49c961 HTTP/1.1
            # check_flow.append(self.facebook_ota())
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
                    options=["is_pull_to_refresh"] if pull_to_refresh is True else []
                )
            )  # Random pull_to_refresh :)
            check_flow.append(
                self.get_reels_tray_feed(
                    reason="pull_to_refresh"
                    if pull_to_refresh is True
                    else "cold_start"
                )
            )

            is_session_expired = (time.time() - self.last_login) > app_refresh_interval
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
                "Error loginin, exception raised: {}\n{}".format(
                    e, traceback.format_exc()
                )
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
        print(os.path.join(self.base_path, fname))

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
                self.cookie_dict["urlgen"]

            if load_uuid:
                self.logger.debug("Loading uuids")
                self.phone_id = data["uuids"]["phone_id"]
                self.uuid = data["uuids"]["uuid"]
                self.client_session_id = data["uuids"]["client_session_id"]
                self.advertising_id = data["uuids"]["advertising_id"]
                self.device_id = data["uuids"]["device_id"]

                self.device_settings = data["device_settings"]
                self.user_agent = data["user_agent"]

            msg = (
                "Recovery from {}: COOKIE {} - UUIDs {} - TIMING, DEVICE "
                "and ...\n- user-agent={}\n- phone_id={}\n- uuid={}\n- "
                "client_session_id={}\n- device_id={}"
            )

            self.logger.info(
                msg.format(
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
