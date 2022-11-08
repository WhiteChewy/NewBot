import datetime


class User():
    def __init__(self):
        self.name = ''
        self.gender = ''
        self.birthdate = datetime.date
        self.city = ''
        self.reason = ''
        self.profile_photo = ''
        self.other_photos = []


    def set_name(self, name):
        self.name = name