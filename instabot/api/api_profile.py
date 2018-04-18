import json


def remove_profile_picture(self):
    data = json.dumps({
        '_uuid': self.uuid,
        '_uid': self.user_id,
        '_csrftoken': self.token
    })
    return self.send_request('accounts/remove_profile_picture/', self.generate_signature(data))


def set_private_account(self):
    data = json.dumps({
        '_uuid': self.uuid,
        '_uid': self.user_id,
        '_csrftoken': self.token
    })
    return self.send_request('accounts/set_private/', self.generate_signature(data))


def set_public_account(self):
    data = json.dumps({
        '_uuid': self.uuid,
        '_uid': self.user_id,
        '_csrftoken': self.token
    })
    return self.send_request('accounts/set_public/', self.generate_signature(data))


def set_name_and_phone(self, name='', phone=''):
    data = json.dumps({
        '_uuid': self.uuid,
        '_uid': self.user_id,
        'first_name': name,
        'phone_number': phone,
        '_csrftoken': self.token
    })
    return self.send_request('accounts/set_phone_and_name/', self.generate_signature(data))


def get_profile_data(self):
    data = json.dumps({
        '_uuid': self.uuid,
        '_uid': self.user_id,
        '_csrftoken': self.token
    })
    return self.send_request('accounts/current_user/?edit=true', self.generate_signature(data))


def edit_profile(self, url, phone, first_name, biography, email, gender):
    data = json.dumps({
        '_uuid': self.uuid,
        '_uid': self.user_id,
        '_csrftoken': self.token,
        'external_url': url,
        'phone_number': phone,
        'username': self.username,
        'full_name': first_name,
        'biography': biography,
        'email': email,
        'gender': gender,
    })
    return self.send_request('accounts/edit_profile/', self.generate_signature(data))
