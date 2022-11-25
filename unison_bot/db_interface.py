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

#SET DATA (UPDATE table SET field)
async def create_new_user(user_id: int, connection: asyncpg.connection.Connection, name='', 
                        city='', gender='', birthday=datetime.date.today(), reason='',
                        profile_photo='', subscribtion=False, matching_pause=False,
                        reason_to_stop='', was_meeting=False, meeting_reaction='',
                        why_meeting_bad='', payment_url='', is_waiting_payment=False,
                        has_match=False, help=False, first_time=True, comunication_help=False, match_id=0):
    # REGISTRATING NEW USER
    await connection.execute('''INSERT INTO users(user_id, name, city, \
        gender, birthday, reason,\
        profile_photo, subscribtion, matching_pause, \
        reason_to_stop, was_meeting, meeting_reaction, \
        why_meeting_bad, payment_url, is_waiting_payment, \
        has_match, help, first_time, \
        comunication_complain, match_id) VALUES( $1, $2, $3,\
            $4, $5, $6, \
            $7, $8, $9, \
            $10, $11, $12, \
            $13, $14, $15, \
            $16, $17, $18, \
            $19, $20)''',
            user_id, name, city,
            gender, birthday, reason,
            profile_photo, subscribtion, matching_pause,
            reason_to_stop, was_meeting, meeting_reaction,
            why_meeting_bad, payment_url, is_waiting_payment,
            has_match, help, first_time, comunication_help, match_id)
    
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

async def main():
    conn = await asyncpg.connect('postgresql://%s:%s@localhost/bot_tg' % (DB_USER, DB_PASSWORD))
    await conn.execute('''
            CREATE TABLE IF NOT EXISTS users(
                user_id bigint PRIMARY KEY,
                name text,
                city text,
                gender char,
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
                match_id bigint
            )
    ''')

    # await conn.execute('''INSERT INTO users(user_id, name, city, \
    #     gender, birthday, reason,\
    #     profile_photo, subscribtion, matching_pause, \
    #     reason_to_stop, was_meeting, meeting_reaction, \
    #     why_meeting_bad, payment_url, is_waiting_payment, \
    #     has_match, help, first_time, \
    #     comunication_complain, match_id) VALUES( $1, $2, $3,\
    #         $4, $5, $6, \
    #         $7, $8, $9, \
    #         $10, $11, $12, \
    #         $13, $14, $15, \
    #         $16, $17, $18, \
    #         $19, $20)''', 
    #     877505237,
    #     'Никита',
    #     'Санкт-Петербург',
    #     'М',
    #     datetime.date(1996, 8, 7),
    #     'Серьезные отношения',
    #     './pic/profiles/877505237/main_profile_photo.jpg',
    #     True,
    #     False,
    #     'null',
    #     False,
    #     'null',
    #     'null',
    #     'null',
    #     False,
    #     True,
    #     False,
    #     True,
    #     False,
    #     5951187826)

    # await conn.execute('''INSERT INTO users(user_id, name, city, \
    #     gender, birthday, reason,\
    #     profile_photo, subscribtion, matching_pause, \
    #     reason_to_stop, was_meeting, meeting_reaction, \
    #     why_meeting_bad, payment_url, is_waiting_payment, \
    #     has_match, help, first_time, \
    #     comunication_complain, match_id) VALUES( $1, $2, $3,\
    #         $4, $5, $6, \
    #         $7, $8, $9, \
    #         $10, $11, $12, \
    #         $13, $14, $15, \
    #         $16, $17, $18, \
    #         $19, $20)''',
    #         5951187826,
    #         'Ефим',
    #         'Санкт-Петербург',
    #         'М',
    #         datetime.date(1992, 6, 14),
    #         'Серьезные отношения',
    #         './pic/Head.png',
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
    #         877505237)
    await conn.close()

asyncio.get_event_loop().run_until_complete(main())
