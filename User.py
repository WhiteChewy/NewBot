import datetime
from dataclasses import dataclass

@dataclass
class User:
    fname: str = ''
    gender: chr = ''
    birthdate: datetime.date = datetime.date.today()
    city: str = ''
    reason: str = ''
    profile_photo: str = ''
    other_photos: tuple = ()