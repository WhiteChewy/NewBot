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
    first_photo: str = ''
    second_photo: str = ''
    third_photo: str = ''