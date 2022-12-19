import asyncio
import asyncpg
import datetime
from config import DB_PASSWORD, DB_USER

async def get_user_id(id: int, connection: asyncpg.connection.Connection) -> int:
    row = await connection.fetchrow('SELECT user_id FROM users WHERE user_id=$1', id)
    return row['user_id']

async def get_match_id(id: int, connection: asyncpg.connection.Connection) -> int:
    row = await connection.fetchrow('SELECT match_id FROM users WHERE user_id=$1', id)
    return row['match_id']

async def get_name(id: int, connection: asyncpg.connection.Connection) -> str:
    row =  await connection.fetchrow('SELECT name FROM users WHERE user_id=$1', id)
    return row['name']

async def get_city(id: int, connection: asyncpg.connection.Connection) -> str:
    row = await connection.fetchrow('SELECT city FROM users WHERE user_id=$1', id)
    return row['city']

async def get_gender(id: int, connection: asyncpg.connection.Connection) -> str:
    row = await connection.fetchrow('SELECT gender FROM users WHERE user_id=$1', id)
    return row['gender']

async def get_birthday(id: int, connection: asyncpg.connection.Connection) -> datetime.date:
    row = await connection.fetchrow('SELECT birthday FROM users WHERE user_id=$1', id)
    return row['birthday']

async def get_reason(id: int, connection: asyncpg.connection.Connection) -> str:
    row = await connection.fetchrow('SELECT reason FROM users WHERE user_id=$1', id)
    return row['reason']

async def get_profile_photo(id: int, connection: asyncpg.connection.Connection) -> str:
    row = await connection.fetchrow('SELECT profile_photo FROM users WHERE user_id=$1', id)
    return row['profile_photo']

async def is_subscribed(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT subscribtion FROM users WHERE user_id=$1', id)
    return row['subscribtion']

async def is_paused(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT matching_pause FROM users WHERE user_id=$1', id)
    return row['matching_pause']

async def get_reason_to_stop(id: int, connection: asyncpg.connection.Connection) -> str:
    row = await connection.fetchrow('SELECT reason_to_stop FROM users WHERE user_id=$1', id)
    return row['reason_to_stop']

async def is_meeting(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT was_meeting FROM users WHERE user_id=$1', id)
    return row['was_meeting']

async def get_meeting_reaction(id: int, connection: asyncpg.connection.Connection) -> str:
    row = await connection.fetchrow('SELECT meeting_reaction FROM users WHERE user_id=$1', id)
    return row['meeting_reaction']

async def get_why_meeting_bad(id: int, connection: asyncpg.connection.Connection) -> str:
    row = await connection.fetchrow('SELECT why_meeting_bad FROM users WHERE user_id=$1', id)
    return row['why_meeting_bad']

async def get_payment_url(id: int, connection: asyncpg.connection.Connection) -> str:
    row = await connection.fetchrow('SELECT payment_url FROM users WHERE user_id=$1', id)
    return row['payment_url']

async def is_waiting_payment(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT is_waiting_payment FROM users WHERE user_id=$1', id)
    return row['is_waiting_payment']

async def is_matching(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT has_match FROM users WHERE user_id=$1', id)
    return row['has_match']

async def is_help(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT help FROM users WHERE user_id=$1', id)
    return row['help']

async def is_first_time(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT first_time FROM users WHERE user_id=$1', id)
    return row['first_time']

async def is_comunication_complain(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT comunication_complain FROM users WHERE user_id=$1', id)
    return row['comunication_complain']

async def get_1st_extra_photo(id: int, connection: asyncpg.connection.Connection) -> str:
    row = await connection.fetchrow('SELECT first_extra_photo FROM users WHERE user_id=$1', id)
    return row['first_extra_photo']

async def get_2nd_extra_photo(id: int, connection: asyncpg.connection.Connection) -> str:
    row = await connection.fetchrow('SELECT second_extra_photo FROM users WHERE user_id=$1', id)
    return row['second_extra_photo']

async def get_3rd_extra_photo(id: int, connection: asyncpg.connection.Connection) -> str:
    row = await connection.fetchrow('SELECT third_extra_photo FROM users WHERE user_id=$1', id)
    return row['third_extra_photo']

async def is_moderated(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT is_moderated FROM users WHERE user_id=$1', id)
    return row['is_moderated']

async def is_first_time_moderated(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT is_first_time_moderated FROM users WHERE user_id=$1', id)
    return row['is_first_time_moderated']

async def is_photo_ok(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT is_photo_ok FROM users WHERE user_id=$1', id)
    return row['is_photo_ok']

async def is_info_ok(id: int, connection: asyncpg.connection.Connection) -> bool:
    row = await connection.fetchrow('SELECT is_info_ok FROM users WHERE user_id=$1', id)
    return row['is_info_ok']

async def get_algorithm_steps(id: int, connection: asyncpg.connection.Connection) -> int:
    row = await connection.fetchrow('SELECT algorithm_steps FROM users WHERE user_id=$1', id)
    return int(row['algorithm_steps'])

async def get_likes(id: int, connection: asyncpg.connection.Connection) -> int:
    row = await connection.fetchrow('SELECT likes FROM users WHERE user_id=$1', id)
    return row['likes']

async def get_super_likes(id: int, connection: asyncpg.connection.Connection) -> int:
    row = await connection.fetchrow('SELECT super_likes FROM users WHERE user_id=$1', id)
    return row['super_likes']

async def get_b64_profile_photo(id: int, connection: asyncpg.connection.Connection) -> bytes:
    row = await connection.fetchrow('SELECT b64_profile FROM users WHERE user_id=$1', id)
    return row['b64_profile']

async def get_b64_1st_photo(id: int, connection: asyncpg.connection.Connection) -> bytes:
    row = await connection.fetchrow('SELECT b64_1st FROM users WHERE user_id=$1', id)
    return bytes(row['b64_1st'], encoding='utf-8')

async def get_b64_2nd_photo(id: int, connection: asyncpg.connection.Connection) -> bytes:
    row = await connection.fetchrow('SELECT b64_2nd FROM users WHERE user_id=$1', id)
    return bytes(row['b64_2nd'], encoding='utf-8')

async def get_b64_1st_photo(id: int, connection: asyncpg.connection.Connection) -> bytes:
    row = await connection.fetchrow('SELECT b64_3rd FROM users WHERE user_id=$1', id)
    return bytes(row['b64_3rd'], encoding='utf-8')

async def get_b64_likes_photo_1(id: int, connection: asyncpg.connection.Connection) -> bytes:
    r'''
    Getting base64 bytes string of first image of person user like from database
    '''
    row = await connection.fetchrow('SELECT b64_likes_photo_1 FROM users WHERE user_id=$1', id)
    return bytes(row['b64_likes_photo_1'], encoding='utf-8')

async def get_b64_likes_photo_2(id: int, connection: asyncpg.connection.Connection) -> bytes:
    r'''
    Getting base64 bytes string of second image of person user like from database
    '''
    row = await connection.fetchrow('SELECT b64_likes_photo_2 FROM users WHERE user_id=$1', id)
    return bytes(row['b64_likes_photo_2'], encoding='utf-8')

async def get_b64_likes_photo_3(id: int, connection: asyncpg.connection.Connection) -> bytes:
    r'''
    Getting base64 bytes string of third image of person user like from database
    '''
    row = await connection.fetchrow('SELECT b64_likes_photo_3 FROM users WHERE user_id=$1', id)
    return bytes(row['b64_likes_photo_3'], encoding='utf-8')

async def get_error_status(id: int, connection: asyncpg.connection.Connection) -> bool:
    r'''
    Get error status for input check
    '''
    row = await connection.fetchrow('SELECT error_status FROM users WHERE user_id=$1', id)
    return row['error_status']

#SET DATA (UPDATE table SET field)
async def create_new_user(user_id: int, connection: asyncpg.connection.Connection, name='', city='',
                        gender='', birthday=datetime.date.today(), reason='',
                        profile_photo='', subscribtion=False, matching_pause=False,
                        reason_to_stop='', was_meeting=False,meeting_reaction='',
                        why_meeting_bad='', payment_url='',is_waiting_payment=False,
                        has_match=False, help=False, first_time=True,
                        comunication_help=False, match_id=0, first_extra_photo='',
                        second_extra_photo='', third_extra_photo='', is_moderated=False,
                        is_first_time_moderated=True, is_photo_ok=True, is_info_ok=True,
                        algorithm_steps=30, likes=7, super_likes=5,
                        b64_profile='', b64_1st='', b64_2nd='',
                        b64_3rd='', b64_likes_1 ='', b64_likes_2='',
                        b64_likes_3='', error_status=False):
    # REGISTRATING NEW USER
    await connection.execute('''INSERT INTO users(user_id, name, city,
        gender, birthday, reason,
        profile_photo, subscribtion, matching_pause,
        reason_to_stop, was_meeting, meeting_reaction,
        why_meeting_bad, payment_url, is_waiting_payment,
        has_match, help, first_time,
        comunication_complain, match_id, first_extra_photo,
        second_extra_photo, third_extra_photo, is_moderated,
        is_first_time_moderated, is_photo_ok, is_info_ok,
        algorithm_steps, likes, super_likes,
        b64_profile, b64_1st, b64_2nd,
        b64_3rd, b64_likes_photo_1, b64_likes_photo_2,
        b64_likes_photo_3, error_status) VALUES( $1, $2, $3,
            $4, $5, $6,
            $7, $8, $9,
            $10, $11, $12,
            $13, $14, $15,
            $16, $17, $18,
            $19, $20, $21,
            $22, $23, $24,
            $25, $26, $27,
            $28, $29, $30,
            $31, $32, $33,
            $34, $35, $36,
            $37, $38) ON CONFLICT (user_id) DO NOTHING;''',
            #   1      2    3
            user_id, name, city,
            #  4       5         6
            gender, birthday, reason,
            #       7            8              9
            profile_photo, subscribtion, matching_pause,
            #      10            11            12
            reason_to_stop, was_meeting, meeting_reaction,
            #      13            14            15
            why_meeting_bad, payment_url, is_waiting_payment,
            #   16      17       18
            has_match, help, first_time, 
            #       19            20            21
            comunication_help, match_id, first_extra_photo,
            #       22                  23               24
            second_extra_photo, third_extra_photo, is_moderated,
            #       25                    26          27
            is_first_time_moderated, is_photo_ok, is_info_ok,
            #       28         29        30
            algorithm_steps, likes, super_likes,
            #    31         32       33
            b64_profile, b64_1st, b64_2nd,
            #  34          35         36
            b64_3rd, b64_likes_1, b64_likes_2,
            #  37           38
            b64_likes_3, error_status)
    
async def set_name(id: int, connection: asyncpg.connection.Connection, name: str):
    await connection.execute('UPDATE users SET name=$1 WHERE user_id=$2', name, id)

async def set_city(id: int, connection: asyncpg.connection.Connection, city: str):
    await connection.execute('UPDATE users SET city=$1 WHERE user_id=$2', city, id)

async def set_gender(id: int, connection: asyncpg.connection.Connection, gender: str):
    await connection.execute('UPDATE users SET gender=$1 WHERE user_id=$2', gender, id)

async def set_birthday(id: int, connection: asyncpg.connection.Connection, birthday: datetime.date):
    await connection.execute('UPDATE users SET birthday=$1 WHERE user_id=$2', birthday, id)

async def set_reason(id: int, connection: asyncpg.connection.Connection, reason: str):
    await connection.execute('UPDATE users SET reason=$1 WHERE user_id=$2', reason, id)

async def set_profile_photo(id: int, connection:asyncpg.connection.Connection, photo: str):
    await connection.execute('UPDATE users SET profile_photo=$1 WHERE user_id=$2', photo, id)

async def set_subscribtion_status(id: int, connection: asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET subscribtion=$1 WHERE user_id=$2', status, id)

async def set_matching_pause_status(id: int, connection: asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET matching_pause=$1 WHERE user_id=$2', status, id)

async def set_reason_to_stop(id: int, connection: asyncpg.connection.Connection, reason: str):
    await connection.execute('UPDATE users SET reason_to_stop=$1 WHERE user_id=$2', reason, id)

async def set_meeting_status(id: int, connection: asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET was_meeting=$1 WHERE user_id=$2', status, id)

async def set_meeting_reaction(id: int, connection: asyncpg.connection.Connection, reaction: str):
    await connection.execute('UPDATE users SET meeting_reaction=$1 WHERE user_id=$2', reaction, id)

async def set_why_meeting_bad(id: int, connection: asyncpg.connection.Connection, why: str):
    await connection.execute('UPDATE users SET why_meeting_bad=$1 WHERE user_id=$2', why, id)

async def set_payment_url(id: int, connection: asyncpg.connection.Connection, url: str):
    await connection.execute('UPDATE users payment_url=$1 WHERE user_id=$2', url, id)

async def set_waiting_payment_status(id: int, connection: asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET is_waiting_payment=$1 WHERE user_id=$2', status, id)

async def set_match_status(id: int, connection:asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET has_match=$1 WHERE user_id=$2', status, id)

async def set_help_status(id: int, connection: asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET help=$1 WHERE user_id=$2', status, id)

async def set_first_time_status(id: int, connection: asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET first_time=$1 WHERE user_id=$2', status, id)

async def set_comunication_complain_status(id: int, connection: asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET comunication_complain=$1 WHERE user_id=$2', status, id)

async def set_match_id_manualy(id: int, connection: asyncpg.connection.Connection, match_id: int):
    await connection.execute('UPDATE users SET match_id=$1 WHERE user_id=$2', match_id, id)

async def set_1st_extra_photo(id: int, connection: asyncpg.connection.Connection, photo: str):
    await connection.execute('UPDATE users SET first_extra_photo=$1 WHERE user_id=$2', photo, id)

async def set_2nd_extra_photo(id: int, connection: asyncpg.connection.Connection, photo: str):
    await connection.execute('UPDATE users SET second_extra_photo=$1 WHERE user_id=$2', photo, id)

async def set_3rd_extra_photo(id: int, connection: asyncpg.connection.Connection, photo: str):
    await connection.execute('UPDATE users SET third_extra_photo=$1 WHERE user_id=$2', photo, id)

async def set_moderated_status(id: int, connection: asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET is_moderated=$1 WHERE user_id=$2', status, id)

async def set_first_time_moderated(id: int, connection: asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET is_first_time_moderated=$1 WHERE user_id=$2', status, id)

async def set_photo_status(id: int, connection: asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET is_photo_ok=$1 WHERE user_id=$2', status, id)

async def set_info_status(id: int, connection: asyncpg.connection.Connection, status: bool):
    await connection.execute('UPDATE users SET is_info_ok=$1 WHERE user_id=$2', status, id)

async def set_algorithm_steps(id: int, connection: asyncpg.connection.Connection, step: int):
    await connection.execute('UPDATE users SET algorithm_steps=$1 WHERE user_id=$2', step, id)

async def set_likes(id: int, connection: asyncpg.connection.Connection, step: int):
    await connection.execute('UPDATE users SET likes=$1 WHERE user_id=$2', step, id)

async def set_superlikes(id: int, connection: asyncpg.connection.Connection, step: int):
    await connection.execute('UPDATE users SET super_likes=$1 WHERE user_id=$2', step, id)

async def set_b64_profile_photo(id: int, connection: asyncpg.connection.Connection, b64_string: bytes):
    await connection.execute('UPDATE users SET b64_profile=$1 WHERE user_id=$2', str(b64_string), id)

async def set_b64_1st_photo(id: int, connection: asyncpg.connection.Connection, b64_string: bytes):
    await connection.execute('UPDATE users SET b64_1st=$1 WHERE user_id=$2', str(b64_string), id)

async def set_b64_2nd_photo(id: int, connection: asyncpg.connection.Connection, b64_string: bytes):
    await connection.execute('UPDATE users SET b64_2nd=$1 WHERE user_id=$2', str(b64_string), id)

async def set_b64_3rd_photo(id: int, connection: asyncpg.connection.Connection, b64_string: bytes):
    await connection.execute('UPDATE users SET b64_3rd=$1 WHERE user_id=$2', str(b64_string), id)

async def set_b64_likes_photo_1(id: int, connection: asyncpg.connection.Connection, b64_string: bytes):
    r'''
    save 1st image of peoples who user likes as b64 string format
    '''
    await connection.execute('UPDATE users SET b64_likes_photo_1=$1 WHERE user_id=$2', str(b64_string), id)

async def set_b64_likes_photo_2(id: int, connection: asyncpg.connection.Connection, b64_string: bytes):
    r'''
    save 2nd image of peoples who user likes as b64 string format
    '''
    await connection.execute('UPDATE users SET b64_likes_photo_2=$1 WHERE user_id=$2', str(b64_string), id)

async def set_b64_likes_photo_3(id: int, connection: asyncpg.connection.Connection, b64_string: bytes):
    r'''
    save 3rd image of peoples who user likes as b64 string format
    '''
    await connection.execute('UPDATE users SET b64_likes_photo_3=$1 WHERE user_id=$2', str(b64_string), id)

async def set_error_status(id: int, connection: asyncpg.connection.Connection, status: bool):
    r'''
    Set error flag
    '''
    await connection.execute('UPDATE users SET error_status=$1 WHERE user_id=$2', status, id)

async def table_ini(conn: asyncpg.connection.Connection):
    conn = await asyncpg.connect('postgresql://admin:sasuke007192@localhost/bot_db')
    await conn.execute('''
            CREATE TABLE IF NOT EXISTS users(
                user_id bigint PRIMARY KEY,
                name text,
                city text,
                gender text,
                birthday date,
                reason text,
                profile_photo text,
                subscribtion bool,
                matching_pause bool,
                reason_to_stop text,
                was_meeting bool,
                meeting_reaction text,
                why_meeting_bad text,
                payment_url text,
                is_waiting_payment bool,
                has_match bool,
                help bool,
                first_time bool,
                comunication_complain bool,
                match_id bigint,
                first_extra_photo text,
                second_extra_photo text,
                third_extra_photo text,
                is_moderated bool,
                is_first_time_moderated bool,
                is_photo_ok bool,
                is_info_ok bool,
                algorithm_steps int,
                likes int,
                super_likes int,
                b64_profile text,
                b64_1st text,
                b64_2nd text,
                b64_3rd text,
                b64_likes_photo_1 text,
                b64_likes_photo_2 text,
                b64_likes_photo_3 text,
                error_status bool
            )
    ''')

#     await conn.execute('''INSERT INTO users(user_id, name, city, \
#         gender, birthday, reason,\
#         profile_photo, subscribtion, matching_pause, \
#         reason_to_stop, was_meeting, meeting_reaction, \
#         why_meeting_bad, payment_url, is_waiting_payment, \
#         has_match, help, first_time, \
#         comunication_complain, match_id) VALUES( $1, $2, $3,\
#             $4, $5, $6, \
#             $7, $8, $9, \
#             $10, $11, $12, \
#             $13, $14, $15, \
#             $16, $17, $18, \
#             $19, $20)''', 
#         877505237,
#         'Никита',
#         'Санкт-Петербург',
#         'М',
#         datetime.date(1996, 8, 7),
#         'Серьезные отношения',
#         './pic/profiles/877505237/main_profile_photo.jpg',
#         True,
#         False,
#         'null',
#         False,
#         'null',
#         'null',
#         'null',
#         False,
#         True,
#         False,
#         True,
#         False,
#         5951187826)

#     await conn.execute('''INSERT INTO users(user_id, name, city, \
#         gender, birthday, reason,\
#         profile_photo, subscribtion, matching_pause, \
#         reason_to_stop, was_meeting, meeting_reaction, \
#         why_meeting_bad, payment_url, is_waiting_payment, \
#         has_match, help, first_time, \
#         comunication_complain, match_id) VALUES( $1, $2, $3,\
#             $4, $5, $6, \
#             $7, $8, $9, \
#             $10, $11, $12, \
#             $13, $14, $15, \
#             $16, $17, $18, \
#             $19, $20)''',
#             5951187826,
#             'Ефим',
#             'Санкт-Петербург',
#             'М',
#             datetime.date(1992, 6, 14),
#             'Серьезные отношения',
#             './pic/Head.png',
#             True,
#             False,
#             'null',
#             False,
#             'null',
#             'null',
#             'null',
#             False,
#             True,
#             False,
#             True,
#             False,
#             877505237)
    
#     print(await is_matching(877505237, conn))
#     print(await is_matching(5951187826, conn))

#     await conn.close()

# asyncio.get_event_loop().run_until_complete(table_ini())
