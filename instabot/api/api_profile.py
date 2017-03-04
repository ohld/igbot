import json


def removeProfilePicture(self):
    data = json.dumps({
        '_uuid': self.uuid,
        '_uid': self.user_id,
        '_csrftoken': self.token
    })
    return self.SendRequest('accounts/remove_profile_picture/', self.generateSignature(data))


def setPrivateAccount(self):
    data = json.dumps({
        '_uuid': self.uuid,
        '_uid': self.user_id,
        '_csrftoken': self.token
    })
    return self.SendRequest('accounts/set_private/', self.generateSignature(data))


def setPublicAccount(self):
    data = json.dumps({
        '_uuid': self.uuid,
        '_uid': self.user_id,
        '_csrftoken': self.token
    })
    return self.SendRequest('accounts/set_public/', self.generateSignature(data))


def setNameAndPhone(self, name='', phone=''):
    data = json.dumps({
        '_uuid': self.uuid,
        '_uid': self.user_id,
        'first_name': name,
        'phone_number': phone,
        '_csrftoken': self.token
    })
    return self.SendRequest('accounts/set_phone_and_name/', self.generateSignature(data))


def getProfileData(self):
    data = json.dumps({
        '_uuid': self.uuid,
        '_uid': self.user_id,
        '_csrftoken': self.token
    })
    return self.SendRequest('accounts/current_user/?edit=true', self.generateSignature(data))


def editProfile(self, url, phone, first_name, biography, email, gender):
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
    return self.SendRequest('accounts/edit_profile/', self.generateSignature(data))
