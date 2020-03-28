import base64
import datetime
import hashlib
import hmac
import json
import logging
import os
import random
import sys
import time
import uuid

import pytz
import requests
import requests.utils
import six.moves.urllib as urllib
from requests_toolbelt import MultipartEncoder
from tqdm import tqdm


from . import config, devices
from .api_login import (
    change_device_simulation,
    generate_all_uuids,
    load_uuid_and_cookie,
    login_flow,
    pre_login_flow,
    reinstall_app_simulation,
    save_uuid_and_cookie,
    set_device,
    sync_launcher,
    sync_user_features,
    get_prefill_candidates,
    get_account_family,
    get_zr_token_result,
    banyan,
    igtv_browse_feed,
    creatives_ar_class,
)
from .api_photo import configure_photo, download_photo, upload_photo
from .api_story import configure_story, download_story, upload_story_photo
from .api_video import configure_video, download_video, upload_video
from .prepare import delete_credentials, get_credentials


try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


version_info = sys.version_info[0:3]
is_py2 = version_info[0] == 2
is_py3 = version_info[0] == 3
is_py37 = version_info[:2] == (3, 7)


version = "0.117.0"
current_path = os.path.abspath(os.getcwd())


class API(object):
    def __init__(
        self,
        device=None,
        base_path=current_path + "/config/",
        save_logfile=True,
        log_filename=None,
        loglevel_file=logging.DEBUG,
        loglevel_stream=logging.INFO,
    ):
        # Setup device and user_agent
        self.device = device or devices.DEFAULT_DEVICE

        self.cookie_fname = None
        self.base_path = base_path

        self.is_logged_in = False
        self.last_login = None

        self.last_response = None
        self.total_requests = 0

        # Setup logging
        # instabot_version = Bot.version()
        # self.logger = logging.getLogger("[instabot_{}]".format(instabot_version))
        self.logger = logging.getLogger("instabot version: " + version)

        if not os.path.exists(base_path):
            os.makedirs(base_path)  # create base_path if not exists

        if not os.path.exists(base_path + "/log/"):
            os.makedirs(base_path + "/log/")  # create log folder if not exists

        if save_logfile is True:
            if log_filename is None:
                log_filename = os.path.join(
                    base_path, "log/instabot_{}.log".format(id(self))
                )

            fh = logging.FileHandler(filename=log_filename)
            fh.setLevel(loglevel_file)
            fh.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s (%(module)s) - %(levelname)s - %(message)s"
                )
            )

            self.logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(loglevel_stream)
        ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        self.logger.addHandler(ch)
        self.logger.setLevel(logging.DEBUG)

        self.last_json = None

    def set_user(self, username, password, generate_all_uuids=True, set_device=True):
        self.username = username
        self.password = password

        if set_device is True:
            self.set_device()

        if generate_all_uuids is True:
            self.generate_all_uuids()

    def set_contact_point_prefill(self, usage="prefill"):
        data = json.dumps({"phone_id": self.phone_id, "usage": usage})
        return self.send_request("accounts/contact_point_prefill/", data, login=True)

    def get_suggested_searches(self, _type="users"):
        return self.send_request(
            "fbsearch/suggested_searches/", self.json_data({"type": _type})
        )

    def read_msisdn_header(self, usage="default"):
        data = json.dumps({"device_id": self.uuid, "mobile_subno_usage": usage})
        return self.send_request(
            "accounts/read_msisdn_header/",
            data,
            login=True,
            headers={"X-DEVICE-ID": self.uuid},
        )

    def log_attribution(self, usage="default"):
        data = json.dumps({"adid": self.advertising_id})
        return self.send_request("attribution/log_attribution/", data, login=True)

    # ====== ALL METHODS IMPORT FROM api_login ====== #
    # def sync_device_features(self, login=False):
    # return sync_device_features(self, login)

    def sync_launcher(self, login=False):
        return sync_launcher(self, login)

    def igtv_browse_feed(self):
        return igtv_browse_feed(self)

    def creatives_ar_class(self):
        return creatives_ar_class(self)

    def sync_user_features(self):
        return sync_user_features(self)

    def get_prefill_candidates(self, login=False):
        return get_prefill_candidates(self, login)

    def get_account_family(self):
        return get_account_family(self)

    def get_zr_token_result(self):
        return get_zr_token_result(self)

    def banyan(self):
        return banyan(self)

    def pre_login_flow(self):
        return pre_login_flow(self)

    def login_flow(self, just_logged_in=False, app_refresh_interval=1800):
        return login_flow(self, just_logged_in, app_refresh_interval)

    def set_device(self):
        return set_device(self)

    def generate_all_uuids(self):
        return generate_all_uuids(self)

    def reinstall_app_simulation(self):
        return reinstall_app_simulation(self)

    def change_device_simulation(self):
        return change_device_simulation(self)

    def load_uuid_and_cookie(self, load_uuid=True, load_cookie=True):
        return load_uuid_and_cookie(self, load_uuid=load_uuid, load_cookie=load_cookie)

    def save_uuid_and_cookie(self):
        return save_uuid_and_cookie(self)

    def login(
        self,
        username=None,
        password=None,
        force=False,
        proxy=None,
        use_cookie=True,
        use_uuid=True,
        cookie_fname=None,
        ask_for_code=False,
        set_device=True,
        generate_all_uuids=True,
        is_threaded=False,
    ):
        if password is None:
            username, password = get_credentials(username=username)

        set_device = generate_all_uuids = True
        self.set_user(username, password)
        self.session = requests.Session()

        self.proxy = proxy
        self.set_proxy()  # Only happens if `self.proxy`

        self.cookie_fname = cookie_fname
        if self.cookie_fname is None:
            fmt = "{username}_uuid_and_cookie.json"
            cookie_fname = fmt.format(username=username)
            self.cookie_fname = os.path.join(self.base_path, cookie_fname)

        cookie_is_loaded = False
        msg = "Login flow failed, the cookie is broken. Relogin again."

        if use_cookie is True:
            # try:
            if (
                self.load_uuid_and_cookie(load_cookie=use_cookie, load_uuid=use_uuid)
                is True
            ):
                # Check if the token loaded is valid.
                if self.login_flow(False) is True:
                    cookie_is_loaded = True
                    self.save_successful_login()
                else:
                    self.logger.info(msg)
                    set_device = generate_all_uuids = False
                    force = True

        if not cookie_is_loaded and (not self.is_logged_in or force):
            self.session = requests.Session()
            if use_uuid is True:
                if (
                    self.load_uuid_and_cookie(
                        load_cookie=use_cookie, load_uuid=use_uuid
                    )
                    is False
                ):
                    if set_device is True:
                        self.set_device()
                    if generate_all_uuids is True:
                        self.generate_all_uuids()
            self.pre_login_flow()
            data = json.dumps(
                {
                    "jazoest": "22264",
                    "country_codes": '[{"country_code":"1","source":["default"]}]',
                    "phone_id": self.phone_id,
                    "_csrftoken": self.token,
                    "username": self.username,
                    "adid": "",
                    "guid": self.uuid,
                    "device_id": self.device_id,
                    "google_tokens": "[]",
                    "password": self.password,
                    # "enc_password:" "#PWD_INSTAGRAM:4:TIME:ENCRYPTED_PASSWORD"
                    "login_attempt_count": "0",
                }
            )

            if self.send_request("accounts/login/", data, True):
                self.save_successful_login()
                self.login_flow(True)
                return True

            elif (
                self.last_json.get("error_type", "") == "checkpoint_challenge_required"
            ):
                # self.logger.info("Checkpoint challenge required...")
                if ask_for_code is True:
                    solved = self.solve_challenge()
                    if solved:
                        self.save_successful_login()
                        self.login_flow(True)
                        return True
                    else:
                        self.logger.error(
                            "Failed to login, unable to solve the challenge"
                        )
                        self.save_failed_login()
                        return False
                else:
                    return False
            elif self.last_json.get("two_factor_required"):
                if self.two_factor_auth():
                    self.save_successful_login()
                    self.login_flow(True)
                    return True
                else:
                    self.logger.error("Failed to login with 2FA!")
                    self.save_failed_login()
                    return False
            else:
                self.logger.error(
                    "Failed to login go to instagram and change your password"
                )
                self.save_failed_login()
                delete_credentials()
                return False

    def two_factor_auth(self):
        self.logger.info("Two-factor authentication required")
        two_factor_code = input("Enter 2FA verification code: ")
        two_factor_id = self.last_json["two_factor_info"]["two_factor_identifier"]

        login = self.session.post(
            config.API_URL + "accounts/two_factor_login/",
            data={
                "username": self.username,
                "verification_code": two_factor_code,
                "two_factor_identifier": two_factor_id,
                "password": self.password,
                "device_id": self.device_id,
                "ig_sig_key_version": config.SIG_KEY_VERSION,
            },
            allow_redirects=True,
        )

        if login.status_code == 200:
            resp_json = json.loads(login.text)
            if resp_json["status"] != "ok":
                if "message" in resp_json:
                    self.logger.error("Login error: {}".format(resp_json["message"]))
                else:
                    self.logger.error(
                        ('Login error: "{}" status and' " message {}.").format(
                            resp_json["status"], login.text
                        )
                    )
                return False
            return True
        else:
            self.logger.error(
                (
                    "Two-factor authentication request returns "
                    "{} error with message {} !"
                ).format(login.status_code, login.text)
            )
            return False

    def save_successful_login(self):
        self.is_logged_in = True
        self.last_login = time.time()
        self.logger.info("Logged-in successfully as '{}'!".format(self.username))

    def save_failed_login(self):
        self.logger.info("Username or password is incorrect.")
        delete_credentials()
        sys.exit()

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

    def solve_challenge(self):
        challenge_url = self.last_json["challenge"]["api_path"][1:]
        try:
            self.send_request(challenge_url, None, login=True, with_signature=False)
        except Exception as e:
            self.logger.error("solve_challenge; {}".format(e))
            return False

        choices = self.get_challenge_choices()
        for choice in choices:
            print(choice)
        code = input("Insert choice: ")

        data = json.dumps({"choice": code})
        try:
            self.send_request(challenge_url, data, login=True)
        except Exception as e:
            self.logger.error(e)
            return False

        print("A code has been sent to the method selected, please check.")
        code = input("Insert code: ").replace(" ", "")

        data = json.dumps({"security_code": code})
        try:
            self.send_request(challenge_url, data, login=True)
        except Exception as e:
            self.logger.error(e)
            return False

        worked = (
            ("logged_in_user" in self.last_json)
            and (self.last_json.get("action", "") == "close")
            and (self.last_json.get("status", "") == "ok")
        )

        if worked:
            return True

        self.logger.error("Not possible to log in. Reset and try again")
        return False

    def get_challenge_choices(self):
        last_json = self.last_json
        choices = []

        if last_json.get("step_name", "") == "select_verify_method":
            choices.append("Checkpoint challenge received")
            if "phone_number" in last_json["step_data"]:
                choices.append("0 - Phone")
            if "email" in last_json["step_data"]:
                choices.append("1 - Email")

        if last_json.get("step_name", "") == "delta_login_review":
            choices.append("Login attempt challenge received")
            choices.append("0 - It was me")
            choices.append("0 - It wasn't me")

        if not choices:
            choices.append(
                '"{}" challenge received'.format(last_json.get("step_name", "Unknown"))
            )
            choices.append("0 - Default")

        return choices

    def logout(self, *args, **kwargs):
        if not self.is_logged_in:
            return True
        data = json.dumps({})
        self.is_logged_in = not self.send_request(
            "accounts/logout/", data, with_signature=False
        )
        return not self.is_logged_in

    def set_proxy(self):
        if getattr(self, "proxy", None):
            parsed = urllib.parse.urlparse(self.proxy)
            scheme = "http://" if not parsed.scheme else ""
            self.session.proxies["http"] = scheme + self.proxy
            self.session.proxies["https"] = scheme + self.proxy

    def send_request(
        self,
        endpoint,
        post=None,
        login=False,
        with_signature=True,
        headers=None,
        extra_sig=None,
        timeout_minutes=None,
    ):
        self.set_proxy()  # Only happens if `self.proxy`
        self.session.headers.update(config.REQUEST_HEADERS)
        self.session.headers.update({"User-Agent": self.user_agent})
        if not self.is_logged_in and not login:
            msg = "Not logged in!"
            self.logger.critical(msg)
            raise Exception(msg)
        if headers:
            self.session.headers.update(headers)
        try:
            self.total_requests += 1
            if post is not None:  # POST
                if with_signature:
                    post = self.generate_signature(
                        post
                    )  # Only `send_direct_item` doesn't need a signature
                    if extra_sig is not None and extra_sig != []:
                        post += "&".join(extra_sig)
                # time.sleep(random.randint(1, 2))
                response = self.session.post(config.API_URL + endpoint, data=post)
            else:  # GET
                # time.sleep(random.randint(1, 2))
                response = self.session.get(config.API_URL + endpoint)
        except Exception as e:
            self.logger.warning(str(e))
            return False

        self.last_response = response
        if post is not None:
            self.logger.debug(
                "POST to endpoint: {} returned response: {}".format(endpoint, response)
            )
        else:
            self.logger.debug(
                "GET to endpoint: {} returned response: {}".format(endpoint, response)
            )
        if response.status_code == 200:
            try:
                self.last_json = json.loads(response.text)
                return True
            except JSONDecodeError:
                return False
        else:
            self.logger.debug(
                "Responsecode indicates error; response content: {}".format(
                    response.content
                )
            )
            if response.status_code != 404 and response.status_code != "404":
                self.logger.error(
                    "Request returns {} error!".format(response.status_code)
                )
            try:
                response_data = json.loads(response.text)
                if response_data.get(
                    "message"
                ) is not None and "feedback_required" in str(
                    response_data.get("message").encode("utf-8")
                ):
                    self.logger.error(
                        "ATTENTION!: `feedback_required`"
                        + str(response_data.get("feedback_message").encode("utf-8"))
                    )
                    try:
                        self.last_response = response
                        self.last_json = json.loads(response.text)
                    except Exception:
                        pass
                    return "feedback_required"
            except ValueError:
                self.logger.error(
                    "Error checking for `feedback_required`, "
                    "response text is not JSON"
                )
                self.logger.info("Full Response: {}".format(str(response)))
                try:
                    self.logger.info("Response Text: {}".format(str(response.text)))
                except Exception:
                    pass
            if response.status_code == 429:
                # if we come to this error, add 5 minutes of sleep everytime we hit the 429 error (aka soft bann) keep increasing untill we are unbanned
                if timeout_minutes is None:
                    timeout_minutes = 0
                if timeout_minutes == 15:
                    # If we have been waiting for more than 15 minutes, lets restart.
                    time.sleep(1)
                    self.logger.error(
                        "Since we hit 15 minutes of time outs, we have to restart. Removing session and cookies. Please relogin."
                    )
                    delete_credentials()
                    sys.exit()
                timeout_minutes += 5
                self.logger.warning(
                    "That means 'too many requests'. I'll go to sleep "
                    "for {} minutes.".format(timeout_minutes)
                )
                time.sleep(timeout_minutes * 60)
                return self.send_request(
                    endpoint,
                    post,
                    login,
                    with_signature,
                    headers,
                    extra_sig,
                    timeout_minutes,
                )
            if response.status_code == 400:
                response_data = json.loads(response.text)
                if response_data.get("challenge_required"):
                    # Try and fix the challenge required error by totally restarting
                    self.logger.error(
                        "Failed to login go to instagram and change your password"
                    )
                    delete_credentials()
                # PERFORM Interactive Two-Factor Authentication
                if response_data.get("two_factor_required"):
                    try:
                        self.last_response = response
                        self.last_json = json.loads(response.text)
                    except Exception:
                        self.logger.error("Error unknown send request 400 2FA")
                        pass
                    return self.two_factor_auth()
                # End of Interactive Two-Factor Authentication
                else:
                    msg = "Instagram's error message: {}"
                    self.logger.info(msg.format(response_data.get("message")))
                    if "error_type" in response_data:
                        msg = "Error type: {}".format(response_data["error_type"])
                    self.logger.info(msg)

            # For debugging
            try:
                self.last_response = response
                self.last_json = json.loads(response.text)
            except Exception:
                self.logger.error("Error unknown send request")
                pass
            return False

    @property
    def cookie_dict(self):
        return self.session.cookies.get_dict()

    @property
    def token(self):
        return self.cookie_dict["csrftoken"]

    @property
    def user_id(self):
        return self.cookie_dict["ds_user_id"]

    @property
    def rank_token(self):
        return "{}_{}".format(self.user_id, self.uuid)

    @property
    def default_data(self):
        return {"_uuid": self.uuid, "_uid": self.user_id, "_csrftoken": self.token}

    def json_data(self, data=None):
        """Adds the default_data to data and dumps it to a json."""
        if data is None:
            data = {}
        data.update(self.default_data)
        return json.dumps(data)

    def action_data(self, data):
        _data = {"radio_type": "wifi-none", "device_id": self.device_id}
        data.update(_data)
        return data

    def auto_complete_user_list(self):
        return self.send_request("friendships/autocomplete_user_list/")

    def batch_fetch(self):
        data = {
            "scale": 3,
            "version": 1,
            "vc_policy": "default",
            "surfaces_to_triggers": '{"5734":["instagram_feed_prompt"],'
            + '"4715":["instagram_feed_header"],'
            + '"5858":["instagram_feed_tool_tip"]}',  # noqa
            "surfaces_to_queries": (
                '{"5734":"viewer() {eligible_promotions.trigger_context_v2(<tr'
                "igger_context_v2>).ig_parameters(<ig_parameters>).trigger_nam"
                "e(<trigger_name>).surface_nux_id(<surface>).external_gating_p"
                "ermitted_qps(<external_gating_permitted_qps>).supports_client"
                "_filters(true).include_holdouts(true) {edges {client_ttl_seco"
                "nds,log_eligibility_waterfall,is_holdout,priority,time_range "
                "{start,end},node {id,promotion_id,logging_data,max_impression"
                "s,triggers,contextual_filters {clause_type,filters {filter_ty"
                "pe,unknown_action,value {name,required,bool_value,int_value,s"
                "tring_value},extra_datas {name,required,bool_value,int_value,"
                "string_value}},clauses {clause_type,filters {filter_type,unkn"
                "own_action,value {name,required,bool_value,int_value,string_v"
                "alue},extra_datas {name,required,bool_value,int_value,string_"
                "value}},clauses {clause_type,filters {filter_type,unknown_act"
                "ion,value {name,required,bool_value,int_value,string_value},e"
                "xtra_datas {name,required,bool_value,int_value,string_value}}"
                ",clauses {clause_type,filters {filter_type,unknown_action,val"
                "ue {name,required,bool_value,int_value,string_value},extra_da"
                "tas {name,required,bool_value,int_value,string_value}}}}}},is"
                "_uncancelable,template {name,parameters {name,required,bool_v"
                "alue,string_value,color_value,}},creatives {title {text},cont"
                "ent {text},footer {text},social_context {text},social_context"
                "_images,primary_action{title {text},url,limit,dismiss_promoti"
                "on},secondary_action{title {text},url,limit,dismiss_promotion"
                "},dismiss_action{title {text},url,limit,dismiss_promotion},im"
                'age.scale(<scale>) {uri,width,height}}}}}}","4715":"viewer() '
                "{eligible_promotions.trigger_context_v2(<trigger_context_v2>)"
                ".ig_parameters(<ig_parameters>).trigger_name(<trigger_name>)."
                "surface_nux_id(<surface>).external_gating_permitted_qps(<exte"
                "rnal_gating_permitted_qps>).supports_client_filters(true).inc"
                "lude_holdouts(true) {edges {client_ttl_seconds,log_eligibilit"
                "y_waterfall,is_holdout,priority,time_range {start,end},node {"
                "id,promotion_id,logging_data,max_impressions,triggers,context"
                "ual_filters {clause_type,filters {filter_type,unknown_action,"
                "value {name,required,bool_value,int_value,string_value},extra"
                "_datas {name,required,bool_value,int_value,string_value}},cla"
                "uses {clause_type,filters {filter_type,unknown_action,value {"
                "name,required,bool_value,int_value,string_value},extra_datas "
                "{name,required,bool_value,int_value,string_value}},clauses {c"
                "lause_type,filters {filter_type,unknown_action,value {name,re"
                "quired,bool_value,int_value,string_value},extra_datas {name,r"
                "equired,bool_value,int_value,string_value}},clauses {clause_t"
                "ype,filters {filter_type,unknown_action,value {name,required,"
                "bool_value,int_value,string_value},extra_datas {name,required"
                ",bool_value,int_value,string_value}}}}}},is_uncancelable,temp"
                "late {name,parameters {name,required,bool_value,string_value,"
                "color_value,}},creatives {title {text},content {text},footer "
                "{text},social_context {text},social_context_images,primary_ac"
                "tion{title {text},url,limit,dismiss_promotion},secondary_acti"
                "on{title {text},url,limit,dismiss_promotion},dismiss_action{t"
                "itle {text},url,limit,dismiss_promotion},image.scale(<scale>)"
                ' {uri,width,height}}}}}}","5858":"viewer() {eligible_promotio'
                "ns.trigger_context_v2(<trigger_context_v2>).ig_parameters(<ig"
                "_parameters>).trigger_name(<trigger_name>).surface_nux_id(<su"
                "rface>).external_gating_permitted_qps(<external_gating_permit"
                "ted_qps>).supports_client_filters(true).include_holdouts(true"
                ") {edges {client_ttl_seconds,log_eligibility_waterfall,is_hol"
                "dout,priority,time_range {start,end},node {id,promotion_id,lo"
                "gging_data,max_impressions,triggers,contextual_filters {claus"
                "e_type,filters {filter_type,unknown_action,value {name,requir"
                "ed,bool_value,int_value,string_value},extra_datas {name,requi"
                "red,bool_value,int_value,string_value}},clauses {clause_type,"
                "filters {filter_type,unknown_action,value {name,required,bool"
                "_value,int_value,string_value},extra_datas {name,required,boo"
                "l_value,int_value,string_value}},clauses {clause_type,filters"
                " {filter_type,unknown_action,value {name,required,bool_value,"
                "int_value,string_value},extra_datas {name,required,bool_value"
                ",int_value,string_value}},clauses {clause_type,filters {filte"
                "r_type,unknown_action,value {name,required,bool_value,int_val"
                "ue,string_value},extra_datas {name,required,bool_value,int_va"
                "lue,string_value}}}}}},is_uncancelable,template {name,paramet"
                "ers {name,required,bool_value,string_value,color_value,}},cre"
                "atives {title {text},content {text},footer {text},social_cont"
                "ext {text},social_context_images,primary_action{title {text},"
                "url,limit,dismiss_promotion},secondary_action{title {text},ur"
                "l,limit,dismiss_promotion},dismiss_action{title {text},url,li"
                "mit,dismiss_promotion},image.scale(<scale>) {uri,width,height"
                '}}}}}}"}'
            ),  # noqa (Just copied from request)
        }
        data = self.json_data(data)
        return self.send_request("qp/batch_fetch/", data)

    def get_timeline_feed(self, options=[]):
        headers = {
            "X-Ads-Opt-Out": "0",
            "X-DEVICE-ID": self.uuid,
            "X-CM-Bandwidth-KBPS": str(random.randint(2000, 5000)),
            "X-CM-Latency": str(random.randint(1, 5)),
        }
        data = {
            "feed_view_info": "",
            "phone_id": self.phone_id,
            "battery_level": random.randint(25, 100),
            "timezone_offset": datetime.datetime.now(pytz.timezone("CET")).strftime(
                "%z"
            ),
            "_csrftoken": self.token,
            "device_id": self.uuid,
            "request_id": self.device_id,
            "_uuid": self.uuid,
            "is_charging": random.randint(0, 1),
            "will_sound_on": random.randint(0, 1),
            "session_id": self.client_session_id,
            "bloks_versioning_id": "e538d4591f238824118bfcb9528c8d005f2ea3becd947a3973c030ac971bb88e",
        }

        if "is_pull_to_refresh" in options:
            data["reason"] = "pull_to_refresh"
            data["is_pull_to_refresh"] = "1"
        elif "is_pull_to_refresh" not in options:
            data["reason"] = "cold_start_fetch"
            data["is_pull_to_refresh"] = "0"

        if "push_disabled" in options:
            data["push_disabled"] = "true"

        if "recovered_from_crash" in options:
            data["recovered_from_crash"] = "1"

        data = json.dumps(data)
        return self.send_request(
            "feed/timeline/", data, with_signature=False, headers=headers
        )

    def get_megaphone_log(self):
        return self.send_request("megaphone/log/")

    def expose(self):
        data = self.json_data(
            {"id": self.uuid, "experiment": "ig_android_profile_contextual_feed"}
        )
        return self.send_request("qe/expose/", data)

    # ====== PHOTO METHODS ====== #
    def upload_photo(
        self,
        photo,
        caption=None,
        upload_id=None,
        from_video=False,
        force_resize=False,
        options={},
    ):
        """Upload photo to Instagram

        @param photo         Path to photo file (String)
        @param caption       Media description (String)
        @param upload_id     Unique upload_id (String). When None, then
                             generate automatically
        @param from_video    A flag that signals whether the photo is loaded
                             from the video or by itself
                             (Boolean, DEPRECATED: not used)
        @param force_resize  Force photo resize (Boolean)
        @param options       Object with difference options, e.g.
                             configure_timeout, rename (Dict)
                             Designed to reduce the number of function
                             arguments! This is the simplest request object.

        @return Boolean
        """
        return upload_photo(
            self, photo, caption, upload_id, from_video, force_resize, options
        )

    def download_photo(self, media_id, filename, media=False, folder="photos"):
        return download_photo(self, media_id, filename, media, folder)

    def configure_photo(self, upload_id, photo, caption=""):
        return configure_photo(self, upload_id, photo, caption)

    # ====== STORY METHODS ====== #
    def download_story(self, filename, story_url, username):
        return download_story(self, filename, story_url, username)

    def upload_story_photo(self, photo, upload_id=None):
        return upload_story_photo(self, photo, upload_id)

    def configure_story(self, upload_id, photo):
        return configure_story(self, upload_id, photo)

    # ====== VIDEO METHODS ====== #
    def upload_video(
        self, video, caption=None, upload_id=None, thumbnail=None, options={}
    ):
        """Upload video to Instagram

        @param video      Path to video file (String)
        @param caption    Media description (String)
        @param upload_id  Unique upload_id (String). When None, then
                          generate automatically
        @param thumbnail  Path to thumbnail for video (String). When None,
                          then thumbnail is generate automatically
        @param options    Object with difference options, e.g.
                          configure_timeout, rename_thumbnail, rename (Dict)
                          Designed to reduce the number of function arguments!
                          This is the simplest request object.

        @return           Object with state of uploading to
                          Instagram (or False)
        """
        return upload_video(self, video, caption, upload_id, thumbnail, options)

    def download_video(self, media_id, filename, media=False, folder="video"):
        return download_video(self, media_id, filename, media, folder)

    def configure_video(
        self,
        upload_id,
        video,
        thumbnail,
        width,
        height,
        duration,
        caption="",
        options={},
    ):
        """Post Configure Video
        (send caption, thumbnail andmore else to Instagram)

        @param upload_id  Unique upload_id (String). Received
                          from "upload_video"
        @param video      Path to video file (String)
        @param thumbnail  Path to thumbnail for video (String). When None,
                          then thumbnail is generate automatically
        @param width      Width in px (Integer)
        @param height     Height in px (Integer)
        @param duration   Duration in seconds (Integer)
        @param caption    Media description (String)
        @param options    Object with difference options, e.g.
                          configure_timeout, rename_thumbnail, rename (Dict)
                          Designed to reduce the number of function arguments!
                          This is the simplest request object.
        """
        return configure_video(
            self, upload_id, video, thumbnail, width, height, duration, caption, options
        )

    # ====== MEDIA METHODS ====== #
    def edit_media(self, media_id, captionText=""):
        data = self.json_data({"caption_text": captionText})
        url = "media/{media_id}/edit_media/".format(media_id=media_id)
        return self.send_request(url, data)

    def remove_self_tag(self, media_id):
        data = self.json_data()
        url = "media/{media_id}/remove/".format(media_id=media_id)
        return self.send_request(url, data)

    def media_info(self, media_id):
        # data = self.json_data({'media_id': media_id})
        url = "media/{media_id}/info/".format(media_id=media_id)
        return self.send_request(url)

    def archive_media(self, media, undo=False):
        action = "only_me" if not undo else "undo_only_me"
        data = self.json_data({"media_id": media["id"]})
        url = "media/{media_id}/{action}/?media_type={media_type}".format(
            media_id=media["id"], action=action, media_type=media["media_type"]
        )
        return self.send_request(url, data)

    def delete_media(self, media):
        data = self.json_data({"media_id": media.get("id")})
        url = "media/{media_id}/delete/".format(media_id=media.get("id"))
        return self.send_request(url, data)

    def gen_user_breadcrumb(self, size):
        key = "iN4$aGr0m"
        dt = int(time.time() * 1000)

        time_elapsed = random.randint(500, 1500) + size * random.randint(500, 1500)
        text_change_event_count = max(1, size / random.randint(3, 5))

        data = "{size!s} {elapsed!s} {count!s} {dt!s}".format(
            **{
                "size": size,
                "elapsed": time_elapsed,
                "count": text_change_event_count,
                "dt": dt,
            }
        )
        return "{!s}\n{!s}\n".format(
            base64.b64encode(
                hmac.new(
                    key.encode("ascii"), data.encode("ascii"), digestmod=hashlib.sha256
                ).digest()
            ),
            base64.b64encode(data.encode("ascii")),
        )

    def comment(self, media_id, comment_text):
        return self.send_request(
            endpoint="media/{media_id}/comment/".format(media_id=media_id),
            post=self.json_data(
                self.action_data(
                    {
                        "container_module": "comments_v2",
                        "user_breadcrumb": self.gen_user_breadcrumb(len(comment_text)),
                        "idempotence_token": self.generate_UUID(True),
                        "comment_text": comment_text,
                    }
                )
            ),
        )

    def reply_to_comment(self, media_id, comment_text, parent_comment_id):
        data = self.json_data(
            {"comment_text": comment_text, "replied_to_comment_id": parent_comment_id}
        )
        url = "media/{media_id}/comment/".format(media_id=media_id)
        return self.send_request(url, data)

    def delete_comment(self, media_id, comment_id):
        data = self.json_data()
        url = "media/{media_id}/comment/{comment_id}/delete/"
        url = url.format(media_id=media_id, comment_id=comment_id)
        return self.send_request(url, data)

    def get_comment_likers(self, comment_id):
        url = "media/{comment_id}/comment_likers/?".format(comment_id=comment_id)
        return self.send_request(url)

    def get_media_likers(self, media_id):
        url = "media/{media_id}/likers/?".format(media_id=media_id)
        return self.send_request(url)

    def like_comment(self, comment_id):
        data = self.json_data(
            {
                "is_carousel_bumped_post": "false",
                "container_module": "comments_v2",
                "feed_position": "0",
            }
        )
        url = "media/{comment_id}/comment_like/".format(comment_id=comment_id)
        return self.send_request(url, data)

    def unlike_comment(self, comment_id):
        data = self.json_data(
            {
                "is_carousel_bumped_post": "false",
                "container_module": "comments_v2",
                "feed_position": "0",
            }
        )
        url = "media/{comment_id}/comment_unlike/".format(comment_id=comment_id)
        return self.send_request(url, data)

    # From profile => "is_carousel_bumped_post":"false",
    # "container_module":"feed_contextual_profile", "feed_position":"0" # noqa
    # From home/feed => "inventory_source":"media_or_ad",
    # "is_carousel_bumped_post":"false", "container_module":"feed_timeline",
    # "feed_position":"0" # noqa
    def like(
        self,
        media_id,
        double_tap=None,
        container_module="feed_short_url",
        feed_position=0,
        username=None,
        user_id=None,
        hashtag_name=None,
        hashtag_id=None,
        entity_page_name=None,
        entity_page_id=None,
    ):

        data = self.action_data(
            {
                "inventory_source": "media_or_ad",
                "media_id": media_id,
                "radio_type": "wifi-none",
                "container_module": container_module,
                "feed_position": str(feed_position),
                "is_carousel_bumped_post": "false",
            }
        )
        if container_module == "feed_timeline":
            data.update({"inventory_source": "media_or_ad"})
        if username:
            data.update({"username": username, "user_id": user_id})
        if hashtag_name:
            data.update({"hashtag_name": hashtag_name, "hashtag_id": hashtag_id})
        if entity_page_name:
            data.update(
                {"entity_page_name": entity_page_name, "entity_page_id": entity_page_id}
            )
        # if double_tap is None:
        double_tap = random.randint(0, 1)
        json_data = self.json_data(data)
        # TODO: comment out debug log out when done
        self.logger.debug("post data: {}".format(json_data))
        return self.send_request(
            endpoint="media/{media_id}/like/".format(media_id=media_id),
            post=json_data,
            extra_sig=["d={}".format(double_tap)],
            headers={
                "X-IG-WWW-Claim": "hmac.AR1ETv6FsubYON5DwNj_0CLNmbW7hSNR1yIMeXuhHJORN4n7"
            },
        )

    def unlike(self, media_id):
        data = self.json_data(
            {
                "media_id": media_id,
                "radio_type": "wifi-none",
                "is_carousel_bumped_post": "false",
                "container_module": "photo_view_other",
                "feed_position": "0",
            }
        )
        url = "media/{media_id}/unlike/".format(media_id=media_id)
        return self.send_request(url, data)

    def get_media_comments(self, media_id, max_id=""):
        url = "media/{media_id}/comments/".format(media_id=media_id)
        if max_id:
            url += "?max_id={max_id}".format(max_id=max_id)
        return self.send_request(url)

    def explore(self, is_prefetch=False):
        data = {
            "is_prefetch": is_prefetch,
            "is_from_promote": False,
            "timezone_offset": datetime.datetime.now(pytz.timezone("CET")).strftime(
                "%z"
            ),
            "session_id": self.client_session_id,
            "supported_capabilities_new": config.SUPPORTED_CAPABILITIES,
        }
        if is_prefetch:
            data["max_id"] = 0
            data["module"] = "explore_popular"
        data = json.dumps(data)
        return self.send_request("discover/explore/", data)

    def get_username_info(self, user_id):
        url = "users/{user_id}/info/".format(user_id=user_id)
        return self.send_request(url)

    def get_self_username_info(self):
        return self.get_username_info(self.user_id)

    def get_news_inbox(self):
        return self.send_request("news/inbox/")

    def get_recent_activity(self):
        return self.send_request("news/inbox/?limited_activity=true&show_su=true")

    def get_following_recent_activity(self):
        return self.send_request("news")

    def get_user_tags(self, user_id):
        url = (
            "usertags/{user_id}/feed/?rank_token=" "{rank_token}&ranked_content=true&"
        ).format(user_id=user_id, rank_token=self.rank_token)
        return self.send_request(url)

    def get_self_user_tags(self):
        return self.get_user_tags(self.user_id)

    def get_geo_media(self, user_id):
        url = "maps/user/{user_id}/".format(user_id=user_id)
        return self.send_request(url)

    def get_self_geo_media(self):
        return self.get_geo_media(self.user_id)

    def sync_from_adress_book(self, contacts):
        url = "address_book/link/?include=extra_display_name,thumbnails"
        return self.send_request(url, "contacts=" + json.dumps(contacts))

    # ====== FEED METHODS ====== #
    def tag_feed(self, tag):
        url = "feed/tag/{tag}/?rank_token={rank_token}&ranked_content=true&"
        return self.send_request(url.format(tag=tag, rank_token=self.rank_token))

    def get_timeline(self):
        url = "feed/timeline/?rank_token={rank_token}&ranked_content=true&"
        return self.send_request(url.format(rank_token=self.rank_token))

    def get_archive_feed(self):
        url = "feed/only_me_feed/?rank_token={rank_token}&ranked_content=true&"
        return self.send_request(url.format(rank_token=self.rank_token))

    def get_user_feed(self, user_id, max_id="", min_timestamp=None):
        url = (
            "feed/user/{user_id}/?max_id={max_id}&min_timestamp="
            "{min_timestamp}&rank_token={rank_token}&ranked_content=true"
            # noqa
        ).format(
            user_id=user_id,
            max_id=max_id,
            min_timestamp=min_timestamp,
            rank_token=self.rank_token,
        )
        return self.send_request(url)

    def get_self_user_feed(self, max_id="", min_timestamp=None):
        return self.get_user_feed(self.user_id, max_id, min_timestamp)

    def get_hashtag_feed(self, hashtag, max_id=""):
        url = (
            "feed/tag/{hashtag}/?max_id={max_id}"
            "&rank_token={rank_token}&ranked_content=true&"
        ).format(hashtag=hashtag, max_id=max_id, rank_token=self.rank_token)
        return self.send_request(url)

    def get_location_feed(self, location_id, max_id=""):
        url = (
            "feed/location/{location_id}/?max_id={max_id}"
            "&rank_token={rank_token}&ranked_content=true&"
        ).format(location_id=location_id, max_id=max_id, rank_token=self.rank_token)
        return self.send_request(url)

    def get_popular_feed(self):
        url = (
            "feed/popular/?people_teaser_supported=1"
            "&rank_token={rank_token}&ranked_content=true&"
        )
        return self.send_request(url.format(rank_token=self.rank_token))

    def get_liked_media(self, max_id=""):
        url = "feed/liked/?max_id={max_id}".format(max_id=max_id)
        return self.send_request(url)

    # ====== FRIENDSHIPS METHODS ====== #
    def get_user_followings(self, user_id, max_id=""):
        url = (
            "friendships/{user_id}/following/?max_id={max_id}"
            "&ig_sig_key_version={sig_key}&rank_token={rank_token}"
        ).format(
            user_id=user_id,
            max_id=max_id,
            sig_key=config.SIG_KEY_VERSION,
            rank_token=self.rank_token,
        )
        return self.send_request(url)

    def get_self_users_following(self):
        return self.get_user_followings(self.user_id)

    def get_user_followers(self, user_id, max_id=""):
        url = "friendships/{user_id}/followers/?rank_token={rank_token}"
        url = url.format(user_id=user_id, rank_token=self.rank_token)
        if max_id:
            url += "&max_id={max_id}".format(max_id=max_id)
        return self.send_request(url)

    def get_self_user_followers(self):
        return self.followers

    def follow(self, user_id):
        data = self.json_data(self.action_data({"user_id": user_id}))
        self.logger.debug("post data: {}".format(data))
        url = "friendships/create/{user_id}/".format(user_id=user_id)
        return self.send_request(url, data)

    def unfollow(self, user_id):
        data = self.json_data({"user_id": user_id, "radio_type": "wifi-none"})
        url = "friendships/destroy/{user_id}/".format(user_id=user_id)
        return self.send_request(url, data)

    def remove_follower(self, user_id):
        data = self.json_data({"user_id": user_id})
        url = "friendships/remove_follower/{user_id}/".format(user_id=user_id)
        return self.send_request(url, data)

    def block(self, user_id):
        data = self.json_data({"user_id": user_id})
        url = "friendships/block/{user_id}/".format(user_id=user_id)
        return self.send_request(url, data)

    def unblock(self, user_id):
        data = self.json_data({"user_id": user_id})
        url = "friendships/unblock/{user_id}/".format(user_id=user_id)
        return self.send_request(url, data)

    def user_friendship(self, user_id):
        data = self.json_data({"user_id": user_id})
        url = "friendships/show/{user_id}/".format(user_id=user_id)
        return self.send_request(url, data)

    def all_friendship(self, user_id):
        url = "friendships/show_many"
        return self.send_request(url)

    def mute_user(self, user, mute_story=False, mute_posts=False):
        data_dict = {}
        if mute_posts:
            data_dict["target_posts_author_id"] = user
        if mute_story:
            data_dict["target_reel_author_id"] = user
        data = self.json_data(data_dict)
        url = "friendships/mute_posts_or_story_from_follow/"
        return self.send_request(url, data)

    def get_muted_friends(self, muted_content):
        # ToDo update endpoints for posts
        if muted_content == "stories":
            url = "friendships/muted_reels"
        elif muted_content == "posts":
            raise NotImplementedError(
                "API does not support getting friends "
                "with muted {}".format(muted_content)
            )
        else:
            raise NotImplementedError(
                "API does not support getting friends"
                " with muted {}".format(muted_content)
            )

        return self.send_request(url)

    def unmute_user(self, user, unmute_posts=False, unmute_stories=False):
        data_dict = {}
        if unmute_posts:
            data_dict["target_posts_author_id"] = user
        if unmute_stories:
            data_dict["target_reel_author_id"] = user
        data = self.json_data(data_dict)
        url = "friendships/unmute_posts_or_story_from_follow/"
        return self.send_request(url, data)

    def get_pending_friendships(self):
        """Get pending follow requests"""
        url = "friendships/pending/"
        return self.send_request(url)

    def approve_pending_friendship(self, user_id):
        data = self.json_data(
            {
                "_uuid": self.uuid,
                "_uid": self.user_id,
                "user_id": user_id,
                "_csrftoken": self.token,
            }
        )
        url = "friendships/approve/{}/".format(user_id)
        return self.send_request(url, post=data)

    def reject_pending_friendship(self, user_id):
        data = self.json_data(
            {
                "_uuid": self.uuid,
                "_uid": self.user_id,
                "user_id": user_id,
                "_csrftoken": self.token,
            }
        )
        url = "friendships/ignore/{}/".format(user_id)
        return self.send_request(url, post=data)

    def get_direct_share(self):
        return self.send_request("direct_share/inbox/?")

    @staticmethod
    def _prepare_recipients(users, thread_id=None, use_quotes=False):
        if not isinstance(users, list):
            print("Users must be an list")
            return False
        result = {"users": "[[{}]]".format(",".join(users))}
        if thread_id:
            template = '["{}"]' if use_quotes else "[{}]"
            result["thread"] = template.format(thread_id)
        return result

    @staticmethod
    def generate_signature(data):
        body = (
            hmac.new(
                config.IG_SIG_KEY.encode("utf-8"), data.encode("utf-8"), hashlib.sha256
            ).hexdigest()
            + "."
            + urllib.parse.quote(data)
        )
        signature = "signed_body={body}&ig_sig_key_version={sig_key}"
        return signature.format(sig_key=config.SIG_KEY_VERSION, body=body)

    @staticmethod
    def generate_device_id(seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode("utf-8") + volatile_seed.encode("utf-8"))
        return "android-" + m.hexdigest()[:16]

    @staticmethod
    def get_seed(*args):
        m = hashlib.md5()
        m.update(b"".join([arg.encode("utf-8") for arg in args]))
        return m.hexdigest()

    @staticmethod
    def generate_UUID(uuid_type):
        generated_uuid = str(uuid.uuid4())
        if uuid_type:
            return generated_uuid
        else:
            return generated_uuid.replace("-", "")

    def get_total_followers_or_followings(  # noqa: C901
        self,
        user_id,
        amount=None,
        which="followers",
        filter_private=False,
        filter_business=False,
        filter_verified=False,
        usernames=False,
        to_file=None,
        overwrite=False,
    ):
        from io import StringIO

        if which == "followers":
            key = "follower_count"
            get = self.get_user_followers
        elif which == "followings":
            key = "following_count"
            get = self.get_user_followings

        sleep_track = 0
        result = []
        next_max_id = ""
        self.get_username_info(user_id)
        username_info = self.last_json
        if "user" in username_info:
            total = amount or username_info["user"][key]

            if total > 200000:
                print(
                    "Consider temporarily saving the result of this big "
                    "operation. This will take a while.\n"
                )
        else:
            return False
        if filter_business:
            print(
                "--> You are going to filter business accounts. "
                "This will take time! <--"
            )
        if to_file is not None:
            if os.path.isfile(to_file):
                if not overwrite:
                    print("File `{}` already exists. Not overwriting.".format(to_file))
                    return False
                else:
                    print("Overwriting file `{}`".format(to_file))
            with open(to_file, "w"):
                pass
        desc = "Getting {} of {}".format(which, user_id)
        with tqdm(total=total, desc=desc, leave=True) as pbar:
            while True:
                get(user_id, next_max_id)
                last_json = self.last_json
                try:
                    with open(to_file, "a") if to_file is not None else StringIO() as f:
                        for item in last_json["users"]:
                            if filter_private and item["is_private"]:
                                continue
                            if filter_business:
                                time.sleep(2 * random.random())
                                self.get_username_info(item["pk"])
                                item_info = self.last_json
                                if item_info["user"]["is_business"]:
                                    continue
                            if filter_verified and item["is_verified"]:
                                continue
                            if to_file is not None:
                                if usernames:
                                    f.write("{}\n".format(item["username"]))
                                else:
                                    f.write("{}\n".format(item["pk"]))
                            result.append(item)
                            pbar.update(1)
                            sleep_track += 1
                            if sleep_track >= 20000:
                                sleep_time = random.uniform(120, 180)
                                msg = (
                                    "\nWaiting {:.2f} min. " "due to too many requests."
                                ).format(sleep_time / 60)
                                print(msg)
                                time.sleep(sleep_time)
                                sleep_track = 0
                    if not last_json["users"] or len(result) >= total:
                        return result[:total]
                except Exception as e:
                    print("ERROR: {}".format(e))
                    return result[:total]

                if last_json["big_list"] is False:
                    return result[:total]

                next_max_id = last_json.get("next_max_id", "")

    def get_total_followers(self, user_id, amount=None):
        return self.get_total_followers_or_followings(user_id, amount, "followers")

    def get_total_followings(self, user_id, amount=None):
        return self.get_total_followers_or_followings(user_id, amount, "followings")

    def get_total_user_feed(self, user_id, min_timestamp=None):
        return self.get_last_user_feed(
            user_id, amount=float("inf"), min_timestamp=min_timestamp
        )

    def get_last_user_feed(self, user_id, amount, min_timestamp=None):
        user_feed = []
        next_max_id = ""
        while True:
            if len(user_feed) >= float(amount):
                # one request returns max 13 items
                return user_feed[:amount]
            self.get_user_feed(user_id, next_max_id, min_timestamp)
            last_json = self.last_json
            if "items" not in last_json:
                return user_feed
            user_feed += last_json["items"]
            if not last_json.get("more_available"):
                return user_feed
            next_max_id = last_json.get("next_max_id", "")

    def get_total_hashtag_feed(self, hashtag_str, amount=100):
        hashtag_feed = []
        next_max_id = ""

        with tqdm(total=amount, desc="Getting hashtag media.", leave=False) as pbar:
            while True:
                self.get_hashtag_feed(hashtag_str, next_max_id)
                last_json = self.last_json
                if "items" not in last_json:
                    return hashtag_feed[:amount]
                items = last_json["items"]
                try:
                    pbar.update(len(items))
                    hashtag_feed += items
                    if not items or len(hashtag_feed) >= amount:
                        return hashtag_feed[:amount]
                except Exception:
                    return hashtag_feed[:amount]
                next_max_id = last_json.get("next_max_id", "")

    def get_total_self_user_feed(self, min_timestamp=None):
        return self.get_total_user_feed(self.user_id, min_timestamp)

    def get_total_self_followers(self):
        return self.get_total_followers(self.user_id)

    def get_total_self_followings(self):
        return self.get_total_followings(self.user_id)

    def get_total_liked_media(self, scan_rate=1):
        next_id = ""
        liked_items = []
        for _ in range(scan_rate):
            self.get_liked_media(next_id)
            last_json = self.last_json
            next_id = last_json.get("next_max_id", "")
            liked_items += last_json["items"]
        return liked_items

    # ====== ACCOUNT / PERSONAL INFO METHODS ====== #
    def change_password(self, new_password):
        data = self.json_data(
            {
                "old_password": self.password,
                "new_password1": new_password,
                "new_password2": new_password,
            }
        )
        return self.send_request("accounts/change_password/", data)

    def remove_profile_picture(self):
        data = self.json_data()
        return self.send_request("accounts/remove_profile_picture/", data)

    def set_private_account(self):
        data = self.json_data()
        return self.send_request("accounts/set_private/", data)

    def set_public_account(self):
        data = self.json_data()
        return self.send_request("accounts/set_public/", data)

    def set_name_and_phone(self, name="", phone=""):
        return self.send_request(
            "accounts/set_phone_and_name/",
            self.json_data({"first_name": name, "phone_number": phone}),
        )

    def get_profile_data(self):
        data = self.json_data()
        return self.send_request("accounts/current_user/?edit=true", data)

    def edit_profile(self, url, phone, first_name, biography, email, gender):
        data = self.json_data(
            {
                "external_url": url,
                "phone_number": phone,
                "username": self.username,
                "full_name": first_name,
                "biography": biography,
                "email": email,
                "gender": gender,
            }
        )
        return self.send_request("accounts/edit_profile/", data)

    def fb_user_search(self, query):
        url = (
            "fbsearch/topsearch/?context=blended&query={query}"
            "&rank_token={rank_token}"
        )
        return self.send_request(url.format(query=query, rank_token=self.rank_token))

    def search_users(self, query):
        url = (
            "users/search/?ig_sig_key_version={sig_key}"
            "&is_typeahead=true&query={query}&rank_token={rank_token}"
        )
        return self.send_request(
            url.format(
                sig_key=config.SIG_KEY_VERSION, query=query, rank_token=self.rank_token
            )
        )

    def search_username(self, username):
        url = "users/{username}/usernameinfo/".format(username=username)
        return self.send_request(url)

    def search_tags(self, query):
        url = "tags/search/?is_typeahead=true&q={query}" "&rank_token={rank_token}"
        return self.send_request(url.format(query=query, rank_token=self.rank_token))

    def search_location(self, query="", lat=None, lng=None):
        url = (
            "fbsearch/places/?rank_token={rank_token}"
            "&query={query}&lat={lat}&lng={lng}"
        )
        url = url.format(rank_token=self.rank_token, query=query, lat=lat, lng=lng)
        return self.send_request(url)

    def get_user_reel(self, user_id):
        url = "feed/user/{}/reel_media/".format(user_id)
        return self.send_request(url)

    def get_reels_tray_feed(
        self, reason="pull_to_refresh"
    ):  # reason can be = cold_start, pull_to_refresh
        data = {
            "supported_capabilities_new": config.SUPPORTED_CAPABILITIES,
            "reason": reason,
            "_csrftoken": self.token,
            "_uuid": self.uuid,
        }
        data = json.dumps(data)
        return self.send_request("feed/reels_tray/", data)

    def get_reels_media(self):
        data = {
            "supported_capabilities_new": config.SUPPORTED_CAPABILITIES,
            "source": "feed_timeline",
            "_csrftoken": self.token,
            "_uuid": self.uuid,
            "_uid": self.user_id,
            "user_ids": self.user_id,
        }
        data = json.dumps(data)
        return self.send_request("feed/reels_media/", data)

    def push_register(self):
        data = {
            "device_type": "android_mqtt",
            "is_main_push_channel": "true",
            "device_sub_type": "2",
            # TODO find out what &device_token={"k":"eyJwbiI6ImNvbS5pbnN0YWdyYW0uYW5kcm9pZCIsImRpIjoiNzhlNGMxNmQtN2YzNC00NDlkLTg4OWMtMTAwZDg5OTU0NDJhIiwiYWkiOjU2NzMxMDIwMzQxNTA1MiwiY2siOiIxNjgzNTY3Mzg0NjQyOTQifQ==","v":0,"t":"fbns-b64"} is
            "device_token": "",
            "_csrftoken": self.token,
            "guid": self.uuid,
            "_uuid": self.uuid,
            "users": self.user_id,
            "familiy_device_id": "9d9aa0f0-40fe-4524-a920-9910f45ba18d",
        }
        data = json.dumps(data)
        return self.send_request("push/register/", data)

    def media_blocked(self):
        url = "media/blocked/"
        return self.send_request(url)

    def get_users_reel(self, user_ids):
        """
            Input: user_ids - a list of user_id
            Output: dictionary: user_id - stories data.
            Basically, for each user output the same as after
            self.get_user_reel
        """
        url = "feed/reels_media/"
        res = self.send_request(
            url, post=self.json_data({"user_ids": [str(x) for x in user_ids]})
        )
        if res:
            return self.last_json["reels"] if "reels" in self.last_json else []
        return []

    def see_reels(self, reels):
        """
            Input - the list of reels jsons
            They can be aquired by using get_users_reel()
            or get_user_reel() methods
        """
        if not isinstance(reels, list):
            # In case of only one reel as input
            reels = [reels]

        story_seen = {}
        now = int(time.time())
        for i, story in enumerate(
            sorted(reels, key=lambda m: m["taken_at"], reverse=True)
        ):
            story_seen_at = now - min(
                i + 1 + random.randint(0, 2), max(0, now - story["taken_at"])
            )
            story_seen["{!s}_{!s}".format(story["id"], story["user"]["pk"])] = [
                "{!s}_{!s}".format(story["taken_at"], story_seen_at)
            ]

        data = self.json_data(
            {
                "reels": story_seen,
                "_csrftoken": self.token,
                "_uuid": self.uuid,
                "_uid": self.user_id,
            }
        )
        data = self.generate_signature(data)
        return self.session.post(
            "https://i.instagram.com/api/v2/" + "media/seen/", data=data
        ).ok

    def get_user_stories(self, user_id):
        url = "feed/user/{}/story/".format(user_id)
        return self.send_request(url)

    def get_self_story_viewers(self, story_id):
        url = ("media/{}/list_reel_media_viewer/?supported_capabilities_new={}").format(
            story_id, config.SUPPORTED_CAPABILITIES
        )
        return self.send_request(url)

    def get_tv_suggestions(self):
        url = "igtv/tv_guide/"
        return self.send_request(url)

    def get_hashtag_stories(self, hashtag):
        url = "tags/{}/story/".format(hashtag)
        return self.send_request(url)

    def follow_hashtag(self, hashtag):
        data = self.json_data({})
        url = "tags/follow/{}/".format(hashtag)
        return self.send_request(url, data)

    def unfollow_hashtag(self, hashtag):
        data = self.json_data({})
        url = "tags/unfollow/{}/".format(hashtag)
        return self.send_request(url, data)

    def get_tags_followed_by_user(self, user_id):
        url = "users/{}/following_tags_info/".format(user_id)
        return self.send_request(url)

    def get_hashtag_sections(self, hashtag):
        data = self.json_data(
            {
                "supported_tabs": "['top','recent','places']",
                "include_persistent": "true",
            }
        )
        url = "tags/{}/sections/".format(hashtag)
        return self.send_request(url, data)

    def get_media_insight(self, media_id):
        url = ("insights/media_organic_insights/{}/?ig_sig_key_version={}").format(
            media_id, config.IG_SIG_KEY
        )
        return self.send_request(url)

    def get_self_insight(self):
        # TODO:
        url = (
            "insights/account_organic_insights/?"
            "show_promotions_in_landing_page=true&first={}"
        ).format()
        return self.send_request(url)

    # From profile => "module_name":"feed_contextual_profile"
    # From home/feed => "module_name":"feed_timeline"
    def save_media(self, media_id, module_name="feed_timeline"):
        return self.send_request(
            endpoint="media/{media_id}/save/".format(media_id=media_id),
            post=self.json_data(self.action_data({"module_name": module_name})),
        )

    def unsave_media(self, media_id):
        data = self.json_data()
        url = "media/{}/unsave/".format(media_id)
        return self.send_request(url, data)

    def get_saved_medias(self):
        url = "feed/saved/"
        return self.send_request(url)

    def get_loom_fetch_config(self):
        return self.send_request("loom/fetch_config/")

    def get_request_country(self):
        return self.send_request("locations/request_country/")

    def get_linked_accounts(self):
        return self.send_request("linked_accounts/get_linkage_status/")

    def get_profile_notice(self):
        return self.send_request("users/profile_notice/")

    def get_business_branded_content(self):
        return self.send_request(
            "business/branded_content/should_require_professional_account/"
        )

    def get_monetization_products_eligibility_data(self):
        return self.send_request(
            "business/eligibility/get_monetization_products_eligibility_data/?product_types=branded_content"
        )

    def get_cooldowns(self):
        body = self.generate_signature(config.SIG_KEY_VERSION)
        url = ("qp/get_cooldowns/?signed_body={}&ig_sig_key_version={}").format(
            body, config.SIG_KEY_VERSION
        )
        return self.send_request(url)

    def log_resurrect_attribution(self):
        data = {
            "_csrftoken": self.token,
            "_uuid": self.uuid,
            "_uid": self.user_id,
        }
        data = json.dumps(data)
        return self.send_request("attribution/log_resurrect_attribution/", data)

    def store_client_push_permissions(self):
        data = {
            "enabled": "true",
            "_csrftoken": self.token,
            "device_id": self.device_id,
            "_uuid": self.uuid,
        }
        data = json.dumps(data)
        return self.send_request("attribution/log_resurrect_attribution/", data)

    def process_contact_point_signals(self):
        data = {
            "phone_id": self.phone_id,
            "_csrftoken": self.token,
            "_uid": self.user_id,
            "device_id": self.device_id,
            "_uuid": self.uuid,
            "google_tokens": "",
        }
        data = json.dumps(data)
        return self.send_request("accounts/process_contact_point_signals/", data)

    def write_supported_capabilities(self):
        data = {
            "supported_capabilities_new": config.SUPPORTED_CAPABILITIES,
            "_csrftoken": self.token,
            "_uid": self.user_id,
            "_uuid": self.uuid,
        }
        data = json.dumps(data)
        return self.send_request("creatives/write_supported_capabilities/", data)

    def arlink_download_info(self):
        return self.send_request("users/arlink_download_info/?version_override=2.2.1")

    def get_direct_v2_inbox(self):
        return self.send_request(
            "direct_v2/inbox/?visual_message_return_type=unseen&thread_message_limit=10&persistentBadging=true&limit=20"
        )

    def get_direct_v2_inbox2(self):
        return self.send_request(
            "direct_v2/inbox/?visual_message_return_type=unseen&persistentBadging=true&limit=0"
        )

    def topical_explore(self):
        url = (
            "discover/topical_explore/?is_prefetch=true&omit_cover_media=true&use_sectional_payload=true&timezone_offset=0&session_id={}&include_fixed_destinations=true"
        ).format(self.client_session_id)
        return self.send_request(url)

    def notification_badge(self):
        data = {
            "phone_id": self.phone_id,
            "_csrftoken": self.token,
            "user_ids": self.user_id,
            "device_id": self.device_id,
            "_uuid": self.uuid,
        }
        data = json.dumps(data)
        return self.send_request("notifications/badge/", data)

    # ====== DIRECT METHODS ====== #
    def get_inbox_v2(self):
        data = json.dumps(
            {
                "visual_message_return_type": "unseen",
                "persistentBadging": "True",
                "limit": "0",
            }
        )
        return self.send_request("direct_v2/inbox/", data)

    def get_presence(self):
        return self.send_request("direct_v2/get_presence/")

    def get_thread(self, thread_id, cursor_id=None):
        data = json.dumps(
            {"visual_message_return_type": "unseen", "seq_id": "40065", "limit": "10"}
        )
        if cursor_id is not None:
            data["cursor"] = cursor_id
        return self.send_request(
            "direct_v2/threads/{}/".format(thread_id), json.dumps(data)
        )

    def get_ranked_recipients(self, mode, show_threads, query=None):
        data = {
            "mode": mode,
            "show_threads": "false" if show_threads is False else "true",
            "use_unified_inbox": "true",
        }
        if query is not None:
            data["query"] = query
        return self.send_request("direct_v2/ranked_recipients/", json.dumps(data))

    def get_scores_bootstrap(self):
        url = "scores/bootstrap/users/?surfaces={surfaces}"
        url = url.format(
            surfaces='["autocomplete_user_list","coefficient_besties_list_ranking","coefficient_rank_recipient_user_suggestion","coefficient_ios_section_test_bootstrap_ranking","coefficient_direct_recipients_ranking_variant_2"]'
        )
        return self.send_request(url)

    def send_direct_item(self, item_type, users, **options):
        data = {"client_context": self.generate_UUID(True), "action": "send_item"}
        headers = {}
        recipients = self._prepare_recipients(
            users, options.get("thread"), use_quotes=False
        )
        if not recipients:
            return False
        data["recipient_users"] = recipients.get("users")
        if recipients.get("thread"):
            data["thread_ids"] = recipients.get("thread")
        data.update(self.default_data)

        url = "direct_v2/threads/broadcast/{}/".format(item_type)
        text = options.get("text", "")
        if item_type == "link":
            data["link_text"] = text
            data["link_urls"] = json.dumps(options.get("urls"))
        elif item_type == "text":
            data["text"] = text
        elif item_type == "media_share":
            data["text"] = text
            data["media_type"] = options.get("media_type", "photo")
            data["media_id"] = options.get("media_id", "")
        elif item_type == "hashtag":
            data["text"] = text
            data["hashtag"] = options.get("hashtag", "")
        elif item_type == "profile":
            data["text"] = text
            data["profile_user_id"] = options.get("profile_user_id")
        elif item_type == "photo":
            url = "direct_v2/threads/broadcast/upload_photo/"
            filepath = options["filepath"]
            upload_id = str(int(time.time() * 1000))
            with open(filepath, "rb") as f:
                photo = f.read()

            data["photo"] = (
                "direct_temp_photo_%s.jpg" % upload_id,
                photo,
                "application/octet-stream",
                {"Content-Transfer-Encoding": "binary"},
            )

            m = MultipartEncoder(data, boundary=self.uuid)
            data = m.to_string()
            headers.update({"Content-type": m.content_type})

        return self.send_request(url, data, with_signature=False, headers=headers)

    def get_pending_inbox(self):
        url = (
            "direct_v2/pending_inbox/?persistentBadging=true" "&use_unified_inbox=true"
        )
        return self.send_request(url)

    # ACCEPT button in pending request
    def approve_pending_thread(self, thread_id):
        data = self.json_data({"_uuid": self.uuid, "_csrftoken": self.token})
        url = "direct_v2/threads/{}/approve/".format(thread_id)
        return self.send_request(url, post=data)

    # DELETE button in pending request
    def hide_pending_thread(self, thread_id):
        data = self.json_data({"_uuid": self.uuid, "_csrftoken": self.token})
        url = "direct_v2/threads/{}/hide/".format(thread_id)
        return self.send_request(url, post=data)

    # BLOCK button in pending request
    def decline_pending_thread(self, thread_id):
        data = self.json_data({"_uuid": self.uuid, "_csrftoken": self.token})
        url = "direct_v2/threads/{}/decline/".format(thread_id)
        return self.send_request(url, post=data)

    def open_instagram_link(self, link):
        return self.send_request(
            "oembed/?url={}".format(urllib.parse.quote(link, safe=""))
        )
