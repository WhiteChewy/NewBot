import datetime
import aiohttp
import json
from config import DB_PASSWORD, DB_USER


async def get_match_id(id: int) -> int:
    r'''
    Returning users match id as int object
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/match/id', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())
    return json_result['id']


async def get_name(id: int) -> str:
    r'''
    Returning users name as str object
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/name', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())
    return json_result['name']


async def get_city(id: int) -> str:
    r'''
    Returning users city as str object
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/city', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())
    return json_result['city']


async def get_gender(id: int) -> str:
    r'''
    Returning users gender as str object
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/gender', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())
    return json_result['gender']


async def get_birthday(id: int) -> datetime.date:
    r'''
    Returning users birthday as datetime.date object
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/birthday', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())
    birthday = datetime.datetime.strptime(json_result['birthday'], '%Y-%m-%d').date()
    return birthday

async def get_reason(id: int) -> str:
    r'''
    Returning reasons to finding match as str object
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/reason', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

    return json_result['reason']

async def get_profile_photo(id: int) -> str:
    r'''
    Returning profile photo telegram ID as str obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/photo/profile_id', json={
         'id' : id 
         }) as resp: json_result = json.loads(await resp.text())

    return json_result['photo_id']

async def is_subscribed(id: int) -> bool:
    r'''
    Returning subscription status as bool object
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/subscription/end', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())
    end_date = datetime.datetime.strptime(json_result['date'], '%Y-%m-%d').date()
    today = datetime.date.today()
    if end_date >= today:
        return True
    else:
        return False

async def is_paused(id: int) -> bool:
    r'''
    Returning if paused finding match as bool obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/match/paused', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())
    
    return json_result['paused']

async def get_reason_to_stop(id: int) -> str:
    r'''
    Returning reason to stop communication as str obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/communication/reason_to_stop', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['reason_to_stop']

async def is_meeting(id: int ) -> bool:
    r'''
    Returning status of was there meeting or not as bool obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/meeting/status', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['was_meeting']

async def get_meeting_reaction(id: int) -> str:
    r'''
    Returning meeting reaction of user as str obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/meeting/reaction', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['reaction']

async def get_why_meeting_bad(id: int) -> str:
    r'''
    Returning why meeting was bad as str obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/meeting/why_bad', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['reaction']

async def get_payment_url(id: int) -> str:
    r'''
    Returning payment url as str obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/payment/url', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['url']

async def is_waiting_payment(id: int) -> bool:
    r'''
    Returning is user waiting for payment confirming as bool obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/payment/waiting', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['waiting']

async def is_matching(id: int) -> bool:
    r'''
    Returning has user match or not as bool obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/match/status', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['has_match']

async def is_help(id: int) -> bool:
    r'''
    Returning has user match or not as bool obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/help/status', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['waiting_help']

async def is_first_time(id: int) -> bool:
    r'''
    Returning first time user using service or not as bool obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/first_time', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['first_time']

async def is_comunication_complain(id: int) -> bool:
    r'''
    Returning first time user using service or not as bool obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/communication/complain/status', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['complain']

async def get_1st_extra_photo(id: int) -> str:
    r'''
    Returning first side photo telegramID as str obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/photo/side/first_id', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['photo_id']

async def get_2nd_extra_photo(id: int) -> str:
    r'''
    Returning second side photo telegramID as str obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/photo/side/second_id', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['photo_id']

async def get_3rd_extra_photo(id: int) -> str:
    r'''
    Returning third side photo telegramID as str obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/photo/side/third_id', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['photo_id']

async def is_moderated(id: int) -> bool:
    r'''
    Returning is user pass moderation or not as bool obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/moderation/status', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['moderated']

async def is_first_time_moderated(id: int ) -> bool:
    r'''
    Returning is user first time passing moderation or not as bool obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/moderation/first_time', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['first_time']

async def is_photo_ok(id: int) -> bool:
    r'''
    Returning is user photo pass moderation or not as bool obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/moderation/photo_ok', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['photo_ok']

async def is_info_ok(id: int) -> bool:
    r'''
    Returning is user profile information pass moderation or not as bool obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/moderation/info_ok', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['info_ok']

async def get_algorithm_steps(id: int) -> int:
    r'''
    Returning number of algorithm steps as int obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/education/steps', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['step']

async def get_likes(id: int) -> int:
    r'''
    Returning number of likes as int obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/education/likes', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['likes']

async def get_super_likes(id: int) -> int:
    r'''
    Returning number of superlikes as int obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/education/superlikes', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['superlikes']

async def get_b64_profile_photo(id: int) -> bytes:
    r'''
    Returning profile photo encoded bytes64 string as int obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/photo/profile_b64', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return bytes(json_result['b64'], encoding='utf-8')

async def get_b64_1st_photo(id: int) -> bytes:
    r'''
    Returning first side photo encoded bytes64 string as int obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/photo/side/first_b64', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return bytes(json_result['b64'], encoding='utf-8')

async def get_b64_2nd_photo(id: int) -> bytes:
    r'''
    Returning second side photo encoded bytes64 string as int obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/photo/side/second_b64', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return bytes(json_result['b64'], encoding='utf-8')

async def get_b64_3rd_photo(id: int) -> bytes:
    r'''
    Returning third side photo encoded bytes64 string as int obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/photo/side/third_b64', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return bytes(json_result['b64'], encoding='utf-8')

async def get_b64_likes_photo_1(id: int) -> bytes:
    r'''
    Returning first photo for algorithm encoded bytes64 string as int obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/photo/ex/first_photo_b64', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return bytes(json_result['b64'], encoding='utf-8')

async def get_b64_likes_photo_2(id: int) -> bytes:
    r'''
    Returning second photo for algorithm encoded bytes64 string as int obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/photo/ex/second_photo_b64', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return bytes(json_result['b64'], encoding='utf-8')

async def get_b64_likes_photo_3(id: int) -> bytes:
    r'''
    Returning third photo for algorithm encoded bytes64 string as int obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/photo/ex/third_photo_b64', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return bytes(json_result['b64'], encoding='utf-8')

async def get_error_status(id: int) -> bool:
    r'''
    Returning first photo for algorithm encoded bytes64 string as int obj
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/error', json={
        'id' : id
      }) as resp: json_result = json.loads(await resp.text())

      return json_result['error']


async def create_new_user(user_id: int):
    r'''
    Creating new user in database
    '''
    async with aiohttp.ClientSession() as session:
      async with session.get(url='http://86.110.212.247:3333/new_user', json={
        'id' : user_id
      }) as resp: pass
    
    
async def set_name(id: int, name: str):
    r'''
    Set name of user
    id - User ID
    name - Name to set
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/name', json={
            'id' : id,
            'name' : name
        }) as resp: pass


async def set_city(id: int, city: str):
    r'''
    Set city of user
    id - User ID
    city - City to set
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/city', json={
            'id' : id,
            'city' : city
        }) as resp: pass

async def set_gender(id: int, gender: str):
    r'''
    Set gebder of user
    id - User ID
    gender - Gender to set
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/gender', json={
            'id' : id,
            'gender' : gender
        }) as resp: pass

async def set_birthday(id: int, birthday: datetime.date):
    r'''
    Set birthday of user
    id - User ID
    birthday - Gender to set
    '''
    birthday = datetime.date.strftime(birthday, '%d.%m.%Y')
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/birthday', json={
            'id' : id,
            'birthday' : birthday
        }) as resp: pass

async def set_reason(id: int, reason: str):
    r'''
    Set searching match reason of user
    id - User ID
    reason - Reason to set
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/reason', json={
            'id' : id,
            'reason' : reason
        }) as resp: pass

async def set_profile_photo(id: int, photo: str):
    r'''
    Set profile photo telegramID
    id - User ID
    photo - ID to set
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/photo/profile_id', json={
            'id' : id,
            'photo_id' : photo
        }) as resp: pass


async def set_subscription_begin_date(id: int, date: datetime.date):
    r'''
    Set beginnig of subscription date
    id - User ID
    date - date to set
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/subscription/begin', json={
            'id' : id,
            'date' : str(date)
        }) as resp: pass


async def set_subscription_end_date(id: int, date:datetime.date):
    r'''
    Set ending of subscription date
    id - User ID
    date - date to set
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/subscription/end', json={
            'id' : id,
            'date' : str(date)
        }) as resp: pass


async def set_matching_pause_status(id: int , status: bool):
    r'''
    Set matching pause status for user 
    id - User ID
    status - bool
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/match/paused', json={
            'id' : id,
            'pause' : status
        }) as resp: pass

async def set_reason_to_stop(id: int , reason: str):
    r'''
    Set reason of stop communication for user 
    id - User ID
    reason - reason to set
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/communication/reason_to_stop', json={
            'id' : id,
            'reason' : reason
        }) as resp: pass

async def set_meeting_status(id: int , status: bool):
    r'''
    Set meeting status (was or not) for user 
    id - User ID
    status - bool
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/meeting/status', json={
            'id' : id,
            'status' : status
        }) as resp: pass

async def set_meeting_reaction(id: int , reaction: str):
    r'''
    Set callback of meeting for user 
    id - User ID
    reaction - reaction to set
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/meeting/reaction', json={
            'id' : id,
            'reaction' : reaction
        }) as resp: pass

async def set_why_meeting_bad(id: int , why: str):
    r'''
    Set why meeting was bad for user 
    id - User ID
    reaction - reaction to set
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/meeting/why_bad', json={
            'id' : id,
            'reason' : why
        }) as resp: pass

async def set_payment_url(id: int , url: str):
    r'''
    Set why meeting was bad for user 
    id - User ID
    url - set payment url
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/payment/url', json={
            'id' : id,
            'url' : url
        }) as resp: pass

async def set_waiting_payment_status(id: int , status: bool):
    r'''
    Set waiting of payment status for user 
    id - User ID
    status - bool
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/payment/waiting', json={
            'id' : id,
            'status' : status
        }) as resp: pass

async def set_match_status(id: int, status: bool):
    r'''
    Set match status for user 
    id - User ID
    status - bool
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/match/status', json={
            'id' : id,
            'status' : status
        }) as resp: pass

async def set_help_status(id: int , status: bool):
    r'''
    Set waiting for help status for user 
    id - User ID
    status - bool
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/help/status', json={
            'id' : id,
            'status' : status
        }) as resp: pass

async def set_first_time_status(id: int , status: bool):
    r'''
    Set first time using service status for user 
    id - User ID
    status - bool
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/first_time', json={
            'id' : id,
            'status' : status
        }) as resp: pass

async def set_comunication_complain_status(id: int , status: bool):
    r'''
    Set communication complain status for user 
    id - User ID
    status - bool
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/communication/complain/status', json={
            'id' : id,
            'status' : status
        }) as resp: pass

async def set_match_id_manualy(id: int , match_id: int):
    r'''
    Set match ID for user 
    id - User ID
    match_id - Match user ID
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/match/id', json={
            'id' : id,
            'match_id' : match_id
        }) as resp: pass

async def set_1st_extra_photo(id: int , photo: str):
    r'''
    Set first side photo telegramID for user 
    id - User ID
    photo - Photo telegram ID
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/photo/side/first_id', json={
            'id' : id,
            'photo_id' : photo
        }) as resp: pass

async def set_2nd_extra_photo(id: int , photo: str):
    r'''
    Set second side photo telegramID for user 
    id - User ID
    photo - Photo telegram ID
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/photo/side/second_id', json={
            'id' : id,
            'photo_id' : photo
        }) as resp: pass

async def set_3rd_extra_photo(id: int , photo: str):
    r'''
    Set third side photo telegramID for user 
    id - User ID
    photo - Photo telegram ID
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/photo/side/third_id', json={
            'id' : id,
            'photo_id' : photo
        }) as resp: pass

async def set_moderated_status(id: int , status: bool):
    r'''
    Set pass moderation or not status for user 
    id - User ID
    status - bool
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/moderation/status', json={
            'id' : id,
            'status' : status
        }) as resp: pass

async def set_first_time_moderated(id: int , status: bool):
    r'''
    Set first time moderated or not status for user 
    id - User ID
    status - bool
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/moderation/first_time', json={
            'id' : id,
            'status' : status
        }) as resp: pass

async def set_photo_status(id: int , status: bool):
    r'''
    User photo pass moderation or not 
    id - User ID
    status - bool
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/moderation/photo_ok', json={
            'id' : id,
            'status' : status
        }) as resp: pass

async def set_info_status(id: int , status: bool):
    r'''
    User profile info pass moderation or not 
    id - User ID
    status - bool
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/moderation/info_ok', json={
            'id' : id,
            'status' : status
        }) as resp: pass

async def set_algorithm_steps(id: int , step: int):
    r'''
    Set number of steps for algorithm education 
    id - User ID
    step - int number
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/education/steps', json={
            'id' : id,
            'steps' : step
        }) as resp: pass

async def set_likes(id: int , likes: int):
    r'''
    Set number of likes in algorithm education 
    id - User ID
    likes - int number
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/education/likes', json={
            'id' : id,
            'likes' : likes
        }) as resp: pass

async def set_superlikes(id: int , superlikes: int):
    r'''
    Set number of superlikes in algorithm education 
    id - User ID
    likes - int number
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/education/superlikes', json={
            'id' : id,
            'superlikes' : superlikes
        }) as resp: pass

async def set_b64_profile_photo(id: int , b64_string: bytes):
    r'''
    Set profile photo base64 bytes string 
    id - User ID
    b64_string - base64 bytes string
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/photo/profile_b64', json={
            'id' : id,
            'b64' : str(b64_string)
        }) as resp: pass

async def set_b64_1st_photo(id: int , b64_string: bytes):
    r'''
    Set first side photo base64 string 
    id - User ID
    b64_string - base64 bytes string
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/photo/side/first_b64', json={
            'id' : id,
            'b64' : str(b64_string)
        }) as resp: pass

async def set_b64_2nd_photo(id: int , b64_string: bytes):
    r'''
    Set second side photo base64 string 
    id - User ID
    b64_string - base64 bytes string
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/photo/side/second_b64', json={
            'id' : id,
            'b64' : str(b64_string)
        }) as resp: pass

async def set_b64_3rd_photo(id: int , b64_string: bytes):
    r'''
    Set third side photo base64 string 
    id - User ID
    b64_string - base64 bytes string
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/photo/side/third_b64', json={
            'id' : id,
            'b64' : str(b64_string)
        }) as resp: pass

async def set_b64_likes_photo_1(id: int , b64_string: bytes):
    r'''
    save 1st image of peoples who user likes as b64 string format
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/photo/ex/first_photo_b64', json={
            'id' : id,
            'b64' : str(b64_string)
        }) as resp: pass

async def set_b64_likes_photo_2(id: int , b64_string: bytes):
    r'''
    save 2nd image of peoples who user likes as b64 string format
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/photo/ex/second_photo_b64', json={
            'id' : id,
            'b64' : str(b64_string)
        }) as resp: pass

async def set_b64_likes_photo_3(id: int , b64_string: bytes):
    r'''
    save 3rd image of peoples who user likes as b64 string format
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/photo/ex/third_photo_b64', json={
            'id' : id,
            'b64' : str(b64_string)
        }) as resp: pass

async def set_error_status(id: int , status: bool):
    r'''
    Set error flag
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/error', json={
            'id' : id,
            'status' : status
        }) as resp: pass

async def table_ini():
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://86.110.212.247:3333/ini') as resp: pass
