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


def get_prefill_candidates(self):
    data = {
        "android_device_id": self.device_id,
        "phone_id": self.phone_id,
        "usages": '[\"account_recovery_omnibox\"]',
        "_csrftoken": self.token,
        "device_id": self.device_id,
    }
    data = json.dumps(data)
    return self.send_request("accounts/get_prefill_candidates/", data)


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


# ====== LOGIN/PRE FLOWS METHODS ====== #


def pre_login_flow(self):
    self.logger.info("Not yet logged in starting: PRE-LOGIN FLOW!")

    self.set_contact_point_prefill("prefill")
    self.sync_launcher(True)
    self.sync_device_features(True)
    # self.get_prefill_candidates()
    self.set_contact_point_prefill("prefill")
    self.sync_launcher(True)
    self.sync_device_features(True)

    # REMOVED: this is not used anymore by the API
    # self.read_msisdn_header("default")
    # self.log_attribution()


# DO NOT MOVE ANY OF THE ENDPOINTS THEYRE IN THE CORRECT ORDER
def login_flow(self, just_logged_in=False, app_refresh_interval=1800):
    self.logger.info("LOGIN FLOW! Just logged-in: {}".format(just_logged_in))
    check_flow = []
    if just_logged_in:
        try:
            # SYNC
            check_flow.append(self.sync_launcher(False))
            check_flow.append(self.get_account_family())
            check_flow.append(self.get_zr_token_result())
            check_flow.append(self.sync_user_features())

            # TODO fix banyan
            # /api/v1/banyan/banyan/?views=["story_share_sheet","threads_people_picker","group_stories_share_sheet","reshare_share_sheet"]
            # check_flow.append(self.banyan())

            # Update feed and timeline
            check_flow.append(self.get_reels_tray_feed(reason="cold_start"))
            check_flow.append(self.get_timeline_feed())

            # TODO fix invalid reel id list
            # signed_body=0afe4f292ac425ff302808c76d93989524b25074ea77e5794edadf72e0328bc6.{"supported_capabilities_new":"[{\"name\":\"SUPPORTED_SDK_VERSIONS\",\"value\":\"45.0,46.0,47.0,48.0,49.0,50.0,51.0,52.0,53.0,54.0,55.0,56.0,57.0,58.0,59.0,60.0,61.0,62.0,63.0,64.0,65.0,66.0,67.0,68.0,69.0,70.0,71.0,72.0,73.0,74.0,75.0,76.0,77.0,78.0,79.0,80.0,81.0\"},{\"name\":\"FACE_TRACKER_VERSION\",\"value\":\"14\"},{\"name\":\"COMPRESSION\",\"value\":\"ETC2_COMPRESSION\"},{\"name\":\"world_tracker\",\"value\":\"world_tracker_enabled\"}]","source":"feed_timeline","_csrftoken":"mmdoMLXFQEzt2w5xLbfm0FTs7gIgqAlc","_uid":"3149016955","_uuid":"f87b5e9f-0663-42f8-9213-ec72cb49c961","user_ids":["283072796","10680697486","25529439127","218694379","3149016955","33167882"]}&ig_sig_key_version=4
            # check_flow.append(self.get_reels_media())

            # TODO fix no token provided
            # device_type=android_mqtt&is_main_push_channel=true&device_sub_type=2&device_token={"k":"eyJwbiI6ImNvbS5pbnN0YWdyYW0uYW5kcm9pZCIsImRpIjoiNzhlNGMxNmQtN2YzNC00NDlkLTg4OWMtMTAwZDg5OTU0NDJhIiwiYWkiOjU2NzMxMDIwMzQxNTA1MiwiY2siOiIxNjgzNTY3Mzg0NjQyOTQifQ==","v":0,"t":"fbns-b64"}&_csrftoken=mmdoMLXFQEzt2w5xLbfm0FTs7gIgqAlc&guid=f87b5e9f-0663-42f8-9213-ec72cb49c961&_uuid=f87b5e9f-0663-42f8-9213-ec72cb49c961&users=3149016955&family_device_id=9d9aa0f0-40fe-4524-a920-9910f45ba18d
            # check_flow.append(self.push_register())

            # TODO fix invalid reel id list
            # signed_body=0afe4f292ac425ff302808c76d93989524b25074ea77e5794edadf72e0328bc6.{"supported_capabilities_new":"[{\"name\":\"SUPPORTED_SDK_VERSIONS\",\"value\":\"45.0,46.0,47.0,48.0,49.0,50.0,51.0,52.0,53.0,54.0,55.0,56.0,57.0,58.0,59.0,60.0,61.0,62.0,63.0,64.0,65.0,66.0,67.0,68.0,69.0,70.0,71.0,72.0,73.0,74.0,75.0,76.0,77.0,78.0,79.0,80.0,81.0\"},{\"name\":\"FACE_TRACKER_VERSION\",\"value\":\"14\"},{\"name\":\"COMPRESSION\",\"value\":\"ETC2_COMPRESSION\"},{\"name\":\"world_tracker\",\"value\":\"world_tracker_enabled\"}]","source":"feed_timeline","_csrftoken":"mmdoMLXFQEzt2w5xLbfm0FTs7gIgqAlc","_uid":"3149016955","_uuid":"f87b5e9f-0663-42f8-9213-ec72cb49c961","user_ids":["283072796","10680697486","25529439127","218694379","3149016955","33167882"]}&ig_sig_key_version=4
            # check_flow.append(self.get_reels_media())
            
            check_flow.append(self.get_loom_fetch_config())

            # getBlockedMedia() ...
            check_flow.append(self.explore(True))
            
            check_flow.append(self.get_recent_activity())
            check_flow.append(self.get_scores_bootstrap())
            check_flow.append(self.get_request_country())

            check_flow.append(self.get_linked_accounts())
            check_flow.append(self.get_business_branded_content())
            check_flow.append(self.get_monetization_products_eligibility_data())

            # TODO FIX request error 405
            # GET /api/v1/qp/get_cooldowns/?signed_body=a7c6081ee2ae5b41a1475f83b6dbc8f1130c67d472f69748221468e1621823b5.%7B%7D&ig_sig_key_version=4
            # check_flow.append(self.get_cooldowns())

            # TODO FIX missing param
            # signed_body=54ca279b6c0daf5f59ce9ba2634e2dad5c46198b5623250e636ee99141b27cae.{"_csrftoken":"mmdoMLXFQEzt2w5xLbfm0FTs7gIgqAlc","_uid":"3149016955","_uuid":"f87b5e9f-0663-42f8-9213-ec72cb49c961"}&ig_sig_key_version=4
            # check_flow.append(self.log_resurrect_attribution())

            check_flow.append(self.arlink_download_info())
            check_flow.append(self.get_username_info(self.user_id))


            # TODO add accounts/process_contact_point_signals/
            # signed_body=2f3d07b0483aefae12d54abf5572d8499b8c878d5939f072522fcf3954cf313c.{"phone_id":"9d9aa0f0-40fe-4524-a920-9910f45ba18d","_csrftoken":"mmdoMLXFQEzt2w5xLbfm0FTs7gIgqAlc","_uid":"3149016955","device_id":"f87b5e9f-0663-42f8-9213-ec72cb49c961","_uuid":"f87b5e9f-0663-42f8-9213-ec72cb49c961","google_tokens":"[]"}&ig_sig_key_version=4
            # check_flow.append(self.process_contact_point_signals())

            check_flow.append(self.get_presence())
            check_flow.append(self.get_inbox_v2())

            # TODO add store_client_push_permissions
            # enabled=true&_csrftoken=mmdoMLXFQEzt2w5xLbfm0FTs7gIgqAlc&device_id=f87b5e9f-0663-42f8-9213-ec72cb49c961&_uuid=f87b5e9f-0663-42f8-9213-ec72cb49c961
            # check_flow.append(self.store_client_push_permissions())

            check_flow.append(self.get_inbox_v2())

            # TODO add write_supported_capabilities
            # signed_body=2a39531abaca22a8cfd87f13633ca08442dc1dfd1af9a15a456eb134c7ecb383.{"supported_capabilities_new":"[{\"name\":\"SUPPORTED_SDK_VERSIONS\",\"value\":\"45.0,46.0,47.0,48.0,49.0,50.0,51.0,52.0,53.0,54.0,55.0,56.0,57.0,58.0,59.0,60.0,61.0,62.0,63.0,64.0,65.0,66.0,67.0,68.0,69.0,70.0,71.0,72.0,73.0,74.0,75.0,76.0,77.0,78.0,79.0,80.0,81.0\"},{\"name\":\"FACE_TRACKER_VERSION\",\"value\":\"14\"},{\"name\":\"COMPRESSION\",\"value\":\"ETC2_COMPRESSION\"},{\"name\":\"world_tracker\",\"value\":\"world_tracker_enabled\"}]","_csrftoken":"mmdoMLXFQEzt2w5xLbfm0FTs7gIgqAlc","_uid":"3149016955","_uuid":"f87b5e9f-0663-42f8-9213-ec72cb49c961"}&ig_sig_key_version=4
            # check_flow.append(self.write_supported_capabilities())

            # TODO add topical_explore
            # /api/v1/discover/topical_explore/?is_prefetch=true&omit_cover_media=true&use_sectional_payload=true&timezone_offset=0&session_id=0f7bf930-4cef-4fde-8ce9-86aea8a7d901&include_fixed_destinations=true HTTP/1.1
            # check_flow.append(self.topical_explore())

            # TODO add notifications/badge
            # phone_id=9d9aa0f0-40fe-4524-a920-9910f45ba18d&_csrftoken=mmdoMLXFQEzt2w5xLbfm0FTs7gIgqAlc&user_ids=3149016955&device_id=f87b5e9f-0663-42f8-9213-ec72cb49c961&_uuid=f87b5e9f-0663-42f8-9213-ec72cb49c961
            # check_flow.append(self.notifications_badge())

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
