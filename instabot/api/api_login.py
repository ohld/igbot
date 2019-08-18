import json
import os
import requests
import requests.utils

from . import config

# ====== SYNC METHODS ====== #
def sync_device_features(self, login=False):
    data = {'id': self.uuid, 'server_config_retrieval': '1', 'experiments': config.LOGIN_EXPERIMENTS}
    if login is False:
        data['_uuid'] = self.uuid
        data['_uid'] = self.user_id
        data['_csrftoken'] = self.token
    data = json.dumps(data)
    return self.send_request('qe/sync/', data, login=login, headers={'X-DEVICE-ID': self.uuid})

def sync_launcher(self, login=False):
    data = {'id': self.uuid, 'server_config_retrieval': '1', 'experiments': config.LAUNCHER_CONFIGS}
    if login is False:
        data['_uuid'] = self.uuid
        data['_uid'] = self.user_id
        data['_csrftoken'] = self.token
    data = json.dumps(data)
    return self.send_request('launcher/sync/', data, login=login)

def sync_user_features(self):
    data = self.default_data
    data['id'] = self.uuid
    data['experiments'] = config.EXPERIMENTS
    data = json.dumps(data)
    self.last_experiments = time.time()
    return self.send_request('qe/sync/', data, headers={'X-DEVICE-ID': self.uuid})

# ====== DEVICE / CLIENT_ID / PHONE_ID AND OTHER VALUES (uuids) ====== #
def set_device(self):
    self.device_settings = devices.DEVICES[self.device]
    self.user_agent = config.USER_AGENT_BASE.format(**self.device_settings)

def generate_all_uuids(self):
    self.phone_id = self.generate_UUID(uuid_type=True)
    self.uuid = self.generate_UUID(uuid_type=True)
    self.client_session_id = self.generate_UUID(uuid_type=True)
    self.advertising_id = self.generate_UUID(uuid_type=True)
    self.device_id = self.generate_device_id(self.get_seed(self.generate_UUID(uuid_type=True)))
    # self.logger.info("uuid GENERATE! phone_id={}, uuid={}, session_id={}, device_id={}".format( self.phone_id, self.uuid, self.client_session_id, self.device_id ))

def reinstall_app_simulation(self):
    self.logger.info("Reinstall app simulation, generating new `phone_id`...")
    self.phone_id = self.generate_UUID(uuid_type=True)
    self.save_uuid_and_cookie()
    self.logger.info("New phone_id: {}".format(self.phone_id))

def change_device_simulation(self):
    self.logger.info("Change device simulation")
    self.reinstall_app_simulation()
    self.logger.info("Generating new `android_device_id`...")
    self.device_id = self.generate_device_id(self.get_seed(self.generate_UUID(uuid_type=True)))
    self.save_uuid_and_cookie()
    self.logger.info("New android_device_id: {}".format(self.device_id))

def load_uuid_and_cookie(self):
    if self.cookie_fname is None:
        fname = "{}_uuid_and_cookie.json".format(self.username)
        self.cookie_fname = os.path.join(self.base_path, fname)

    if os.path.isfile(self.cookie_fname) is False:
        return False

    with open(fname, 'r') as f:
        data = json.load(f)
        if 'cookie' in data:
            self.session.cookies = requests.utils.cookiejar_from_dict(data['cookie'])
            cookie_username = self.cookie_dict['ds_user']
            assert cookie_username == self.username

            self.phone_id = data['uuids']['phone_id']
            self.uuid = data['uuids']['uuid']
            self.client_session_id = data['uuids']['client_session_id']
            self.advertising_id = data['uuids']['advertising_id']
            self.device_id = data['uuids']['device_id']

            self.last_login = data['timing_value']['last_login']
            self.last_experiments = data['timing_value']['last_experiments']

            self.device_settings = data['device_settings']
            self.user_agent = data['user_agent']

            self.logger.info('Recovery from {}, COOKIE, TIMING, DEVICE and ... \n- user-agent={}\n- phone_id={}\n- uuid={}\n- client_session_id={}\n- device_id={}'.format(fname, self.user_agent, self.phone_id, self.uuid, self.client_session_id, self.device_id))
        else:
            self.logger.info('The cookie seems to be the with the older structure. Load and init again all uuids')
            self.session.cookies = requests.utils.cookiejar_from_dict(data['cookie'])
            cookie_username = self.cookie_dict['ds_user']
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
        'uuids': {
            'phone_id': self.phone_id,
            'uuid': self.uuid,
            'client_session_id': self.client_session_id,
            'advertising_id': self.advertising_id,
            'device_id': self.device_id
        },
        'cookie': requests.utils.dict_from_cookiejar(self.session.cookies),
        'timing_value': {
            'last_login': self.last_login,
            'last_experiments': self.last_experiments
        },
        'device_settings': self.device_settings,
        'user_agent': self.user_agent
    }
    with open(self.cookie_fname, 'w') as f:
        json.dump(data, f)
