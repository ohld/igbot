import json

from . import config

#====== SYNC BLOCK ======#
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
