# -*- coding: utf-8 -*-
import config
import logging

from User import User
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
user_form = User()

@dp.message_handler(commands='start')
async def show_starting_menu(message: types.Message):
    # start_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    # about_button = types.InlineKeyboardButton('🧾О проекте', callback_data='about')
    # uniqueness_button = types.InlineKeyboardButton('🔮Уникальность', callback_data='uniqueness')
    # imprinting_button = types.InlineKeyboardButton('💡Что такое импринтинг', callback_data='imprint')
    # start_inline_keyboard.row(about_button, uniqueness_button, imprinting_button)
    # user_agreement_button = types.InlineKeyboardButton('📝Соглашение', callback_data='user_agreement')
    # faq_button = types.InlineKeyboardButton('❓Частые вопросы', callback_data='faq')
    # registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='register')
    # start_inline_keyboard.row(user_agreement_button, faq_button, registration_button)
    # await bot.send_message(message.from_user.id, text='Вы можете нажать любую кнопку ниже, и узнать всю необходимую информацию о нашем проекте.', reply_markup=start_inline_keyboard)
    photo = open('./pic/start.jpg', 'rb')
    await bot.send_photo(message.from_user.id, photo)
    starting_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='register')
    about_project_button = types.InlineKeyboardButton('ℹ️ Читать о проекте', callback_data='back')
    starting_inline_keyboard.add(registration_button)
    starting_inline_keyboard.add(about_project_button)
    await bot.send_message(message.from_user.id, text='👋 Добро пожаловать!\n\nСоздайте свой профиль и пройдите небольшой тест, который поможет роботу понять,\
         кто вам действительно подходит.\n\nРобот будет еженедельно подбирать для вас наиболее подходящую пару, с которой вы сможете пообщаться, чтобы лучше узнать друг друга!')
    await bot.send_message(message.from_user.id, text='Начнем знакомство?', reply_markup=starting_inline_keyboard)


@dp.callback_query_handler(text='about')
async def show_about_text(message: types.Message):
    about_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='back')
    about_keyboard.add(registration_button)
    about_keyboard.add(back_button)
    await bot.send_message(message.from_user.id, text='Система знакомств «Unison» основана на специально разработанном алгоритме, имеющем научную основу. \
                                                        Импринтинг или запечатление — это неосознанная привязанность к конкретным образам из подсознания. \
                                                        \nПоиск начнётся сразу после регистрации и будет повторяться каждую неделю. Это время даётся вам \
                                                        для знакомства и общения с кандидатами.', reply_markup=about_keyboard)


@dp.callback_query_handler(text='uniqueness')
async def show_uniqueness(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAEGWz5jatRbDYvJEbfafTUQe_0WBegfIAACygEAAiryOgd8lWEmSYCDFCsE')
    uniqueness_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='back')
    uniqueness_inline_keyboard.add(registration_button)
    uniqueness_inline_keyboard.add(back_button)
    await bot.send_message(message.from_user.id, text='Наверняка вы обращали внимание, что во всех счастливых историях любви партнёры говорят о знакомстве примерно одинаково:\
                                                        \n\n«Непонятное очарование этого человека сразу захватило меня». Наши психологи совместно с программистами проанализировали \
                                                        более 5 000 самых успешных и выдающихся пар, и выявили те неуловимые свойства, которые проявлялись в момент знакомства. \
                                                        \n\nНаша специально обученная нейросеть ©Unison проанализирует внешность и поведенческие параметры по более, чем 100 свойствам,\
                                                         и, исходя из полученных данных и ваших вкусовых предпочтений, сможет подобрать вам лучшую пару.', reply_markup=uniqueness_inline_keyboard)


@dp.callback_query_handler(text='imprint')
async def show_imprint(message: types.Message):
    imprint_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='back')
    imprint_inline_keyboard.add(registration_button)
    imprint_inline_keyboard.add(back_button)
    await bot.send_message(message.from_user.id, text='Импринтинг (от английского «imprinting» — «впечатывание») — это особая форма обучения, во время которой информация\
                                                     запоминается мгновенно и сохраняется на всю жизнь. Она буквально впечатывается в мозг и в дальнейшем проявляется на уровне подсознания.\n\nПоэтому особенности поведения, зафиксированные в процессе импринтинга, сложно контролировать и\
                                                     практически невозможно изменить. Информация, запомненная посредством данного механизма, не требует позитивного подкрепления (не нужно ничего повторять — она и так хранится всю жизнь).', 
                                                     reply_markup=imprint_inline_keyboard)
            

@dp.callback_query_handler(text='user_agreement')
async def show_user_agreement(message: types.Message):
    user_agreement_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='back')
    user_agreement_keyboard.add(registration_button)
    user_agreement_keyboard.add(back_button)
    await bot.send_message(message.from_user.id, text='''Пользовательское соглашение на использование сервиса «UNISON».
Краткое изложение этого документа. 

Если у вас совсем нет времени, мы рекомендуем ознакомиться хотя бы с этим пунктом. Здесь в нескольких тезисах собрана вся необходимая информация о соглашении и правилах использования сервиса. 

- Сервис предназначен для знакомств;
- Если начинаете использовать сервис, то принимаете все правила сервиса;
- Мы используем ваши персональные данные очень аккуратно;
- Персональные данные нужны для работы системы и лучшего поиска потенциального партнёра;
- Мы — единственные в мире используем метод импринтинга в дейтинге (знакомствах);
- Импринтинг — это эффект неосознанного запечатления;
- Наше ноу-хау — система расшифровки импринтинга;
- Мы используем фотографии пользователей, чтобы формировать датасет из фото;
- На основе сопоставлений датасетов по технологии (с) «Unison» мы ищем потенциальных партнёров каждому пользователю сервиса;
- Поиск происходит автоматически и сами сотрудники сервиса не могут влиять на результат поиска;
- Сервис снимает с себя ответственность за адекватность пользователей, соответствие фотографиям и поведение людей, использующих систему;
- Тем не менее, мы прилагаем все усилия, чтобы в сервисе были только доброжелательные и адекватные пользователи, с единственной целью — серьёзные отношения;
- Сервис предоставляет информацию властям в рамках действующего законодательства;
- Оплата в сервисе взимается за предоставление первоочередной возможности поиска потенциальных партнёров и за другие услуги;
- Мы относимся с особым расположением ко всем людям с «нетрадиционной» ориентацией, но работаем в данный момент только для гетеросексуальных пар.

Об этом соглашении.

Этот длинный текст — свод правил, которые мы, компания «UNISON», установили для себя для выстраивания корректных отношений с пользователями сервиса. Мы постарались предусмотреть все случаи разногласий и отказаться от любой ответственности, которая может возникнуть в процессе использования сервиса. 

Мы используем следующие названия: сервис «UNISON», «Unison dating», «Unison bot», технология подбора партнёра (с) «Unison». Это не все наименования, но наиболее часто используемые.

Что такое оферта.

Мы, как компания, действуем на основе оферты — это специальный вид договора, который не требует подписания, чтобы считаться рабочим документом. Для того, чтобы принять этот договор на изложенных ниже условиях, достаточно просто начать использовать наш сервис.

Перед использованием сервиса «UNISON» необходимо ознакомиться с условиями настоящего пользовательского соглашения. Часто многие пользователи в других сервисах просто ставят галочку «принимаю», не читая текст. Вы правы, прочитать весь текст невозможно, но мы настаиваем, чтобы вы сделали это, так как этого требует закон.')
''')
    await bot.send_message(message.from_user.id, text='''Ваше согласие.

Если вы начинаете использовать сервис — значит признаёте согласие с тем, что: 
- До начала использования ознакомились с условиями настоящего пользовательского соглашения в полном объёме и приняли все условия без каких-либо исключений;
- Настоящее пользовательское соглашение может быть изменено Компанией без какого-либо уведомления. Новая редакция пользовательского соглашения вступает в силу с момента её размещения на Сайте и в боте, если иное не предусмотрено новой редакцией соглашения.

В случае несогласия с условиями настоящего пользовательского соглашения пользователю следует прекратить использование сервиса «UNISON».

Как работает система?

UNISON — это система знакомств, то есть сервис предназначен только для знакомств с целью создания семьи и отношений. Все другие способы использования считаются невалидными и пользователи-нарушители  могут быть заблокированы.

Как мы используем ваши фотографии и личные данные?

Для того, чтобы находить лучшего партнёра, мы составляем несколько датасетов. Датасеты — это блоки информации, которую мы обрабатываем собственными алгоритмами. Для таких датасетов необходимо взять несколько фото человека и несколько фото симпатичных ему людей. 

По различным признакам загружаемых фото (размер, дата съёмки, на что снято, редактировалось фото или нет и т.д.) мы определяем степень ценности фото. Используя информацию из открытых источников, мы ищем дубли, тональность и окружение для этих фото. 

Мы не можем вмешиваться в содержимое датасетов и менять алгоритм. Наша задача — перенести без потерь научный метод на практику.

Насколько безопасно предоставлять данные компании «UNISON»?

Предоставлять данные точно так же безопасно, как и в любой другой сервис в России. Мы не используем данные никак, кроме как в описанных алгоритмах.

Права на используемые данные. 

Мы предоставляем право использования наших систем любым пользователям согласно простой (неисключительной) лицензии. То есть вы можете использовать систему как физическое лицо в любой стране, где возможен доступ в систему (и где явно не запрещено такое использование). 

Данные, которыми обладают пользователи и которые пользователи загружают в систему, предоставляются для совместного доступа. Мы обязуемся не нарушать приватность и не публиковать ничего, что могло бы идентифицировать пользователей. Кроме того, пользователь обязуется принимать должные меры для обеспечения безопасности собственных данных (в том числе, персональных данных).

Платные сервисы. 

Для того, чтобы развивать сервис, мы сделали некоторые функционалы платными. Мы получаем оплату и инвестируем её в развитие сервиса. Мы стараемся держать уровень оплаты на таком уровне, чтобы стоимость была доступной для всех. 

Основной платный сервис — предоставление пакета преимущественного права поиска партнёров. Для тех, кто оплатил сервис, доступны расширенные функции системы. Оплата взимается еженедельно или ежемесячно, путём списания с карты, подключенной к оплате.

Для того, чтобы отключить оплату, необходимо изменить настройки системы в платёжной системе, подключенной к тому интерфейсу, который вы используете (например, Телеграмм-бот).

Другие платные сервисы могут быть основаны на других функционалах системы, возможно, не существующие в данный момент, когда вы читаете это соглашение. Они могут иметь также другую схему оплаты, например, единоразовую.'''
)
    await bot.send_message(message.from_user.id, text='''Ответственность. 

Мы отказываемся от какой-либо ответственности (все так делают, просто мы говорим об этом прямо). Обычно говорят, что сервис предоставляется на условиях «как есть» (as is).

Мы не не предоставляем никаких гарантий в отношении безошибочной и бесперебойной работы, соответствия сервиса конкретным целям и ожиданиям пользователя, не гарантируем достоверность, точность, полноту и своевременность предоставляемых сервисом данных, а также не предоставляем никаких иных гарантий, указанных или не указанных в этом соглашении. 

Мы также не несём ответственность за последствия использования или неиспользования сервиса. Однако предупреждаем, что «Под лежачий камень вода не течёт» и «Человек сам кузнец своего счастья». 

Что нельзя. 

Просим не загружать, не хранить, не публиковать, не распространять любую информацию, которая может быть воспринята, как «токсичная», опасная, дискредитирующая, нарушающая неприкосновенность третьих лиц. 

Также нельзя размещать: 
- Рекламу и пропаганду (в том числе рекламу вакансий, образовательных программ и т.д.);
- Что-то непристойное;
- То, что нарушает требования закона.

Актуальность соглашения. 

Действие этого соглашения распространяется на всё, что было ранее, если обновление или новая версия не сопровождается иным соглашением. Это соглашение может быть изменено в любой момент без уведомлений. 

Редакция от 07 октября 2021 года.''',
reply_markup=user_agreement_keyboard)


@dp.callback_query_handler(text='faq')
async def show_faq(message: types.Message):
    faq_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    concept_button = types.InlineKeyboardButton('📊Концепция сервиса', callback_data='concept')
    photo_button = types.InlineKeyboardButton('🖼Фото пользователей', callback_data='photo')
    find_button = types.InlineKeyboardButton('💑Поиск пары и оплата', callback_data='find')
    investors_button = types.InlineKeyboardButton('📈Партнеры и инвесторы', callback_data='investors')
    journalist_button = types.InlineKeyboardButton('📝Для журналистов', callback_data='journalists')
    back_button = types.InlineKeyboardButton('⬅️Назад в главное меню', callback_data='back')
    faq_inline_keyboard.row(concept_button, photo_button)
    faq_inline_keyboard.row(find_button, investors_button)
    faq_inline_keyboard.row(journalist_button, back_button)
    await bot.send_message(message.from_user.id, text='Выберете раздел FAQ.', reply_markup=faq_inline_keyboard)


@dp.callback_query_handler(text='register')
async def show_register(message: types.Message):
    await bot.send_message(message.from_user.id, text='Извините, сюда пока нельзя.')


@dp.callback_query_handler(text='back')
async def show_back(message: types.Message):
    start_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    about_button = types.InlineKeyboardButton('🧾О проекте', callback_data='about')
    uniqueness_button = types.InlineKeyboardButton('🔮Уникальность', callback_data='uniqueness')
    imprinting_button = types.InlineKeyboardButton('💡Что такое импринтинг', callback_data='imprint')
    start_inline_keyboard.row(about_button, uniqueness_button, imprinting_button)
    user_agreement_button = types.InlineKeyboardButton('📝Соглашение', callback_data='user_agreement')
    faq_button = types.InlineKeyboardButton('❓Частые вопросы', callback_data='faq')
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='register')
    start_inline_keyboard.row(user_agreement_button, faq_button, registration_button)
    await bot.send_message(message.from_user.id, text='Вы можете нажать любую кнопку ниже, и узнать всю необходимую информацию о нашем проекте.', 
                            reply_markup=start_inline_keyboard)


@dp.callback_query_handler(text='concept')
async def show_concept(message: types.Message):
    back_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='faq')
    back_inline_keyboard.add(registration_button)
    back_inline_keyboard.add(back_button)
    await bot.send_message(message.from_user.id, text='''❓ Это те знакомства, которые не знакомят, а влюбляют?

✅ Именно так. Наша система построена на научном методе выбора партнёра, это приводит к возникновению любви. Кроме того, мы работаем на результат, а не на повторение дофаминовых циклов, которые вызывают у людей зависимость и приводят в приложения снова и снова.

Мы работаем над формированием правильно сбалансированной пары, в которой будет любовь и согласие на многие годы.

❓ Как работает система?

✅ Основа работы — определение наиболее благоприятного фенотипа с использованием расшифровки импринтинга. Говоря простым языком, мы определяем образ наиболее подходящего человека для каждого пользователя и даём возможность этим людям встретиться в реальной жизни.

❓ Чем отличается Unison от других знакомств?

✅ Популярные системы знакомств, основанные на визуальном фильтре (Тиндер-подобные системы) имеют крайне низкую объективную оценку эффективности знакомств — при кажущейся простоте получения знакомств эти системы не выполняют своих функций.

Мы же, наоборот, стремимся работать именно для достижения цели — знакомство с полностью подходящим человеком с целью начать отношения.''',
reply_markup=back_inline_keyboard)


@dp.callback_query_handler(text='photo')
async def show_photo(message: types.Message):
    photo_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='faq')
    photo_inline_keyboard.add(registration_button)
    photo_inline_keyboard.add(back_button)
    await bot.send_message(message.from_user.id, text='''❓ Кто увидит мои фото?

✅ В системе есть три типа фото, которые загружает сам пользователь. 

Первый тип — собственное фото профиля. Это фото будет видеть только потенциальный партнёр, которого мы подберём для вас. 

Второй тип — собственные «селфи» для формирования датасета. Эти фото не видит никто, кроме нашего алгоритма.

Третий тип — фото наиболее привлекательных для пользователя людей. Эти фото не видит также никто, кроме нашего алгоритма. 

То есть только одно фото увидит ваш потенциальный партнёр — фото профиля.

❓ Как будут использованы мои фотографии?

✅ Фото используются для формирования датасета. Система машинного обучения (искусственный интеллект) сравнивает личный датасет пользователя с датасетами других пользователей и находит наиболее подходящие совпадения.

❓ Вы просите загрузить фото тех, кто мне нравится. Зачем это надо и как они будут использованы?

✅ Нам необходимо понять динамику изменения фенотипических особенностей благоприятных образов. Если таких фотографий нет, результат поиска будет значительно хуже.''', 
reply_markup=photo_inline_keyboard)


@dp.callback_query_handler(text='find')
async def show_find(message: types.Message):
    find_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='faq')
    find_inline_keyboard.add(registration_button)
    find_inline_keyboard.add(back_button)
    await bot.send_message(message.from_user.id, text='''❓ Вы разрушаете браки, потому что предоставляете пользователям лучшие варианты пары, чем они имеют сейчас. Многие могут поверить в чудодейственность вашей системы.

✅ Разрушение несчастливого брака — скорее благо, чем трагедия. Жизнь довольно короткая, чтобы жить в травмирующих и токсичных отношениях. Позвольте себе быть счастливыми и узнать, как это на самом деле — любить и быть любимым.

❓ Сколько и за что надо платить?

✅ На данный момент можно платить за платную подписку, которая предоставляет неограниченные возможности поиска и более широкий выбор партнёров. Актуальную стоимость можно узнать только в момент оплаты. От подписки можно в любой момент отказаться. Все цены подобраны с учётом того, чтобы платный сервис мог себе позволить любой пользователь.

В ближайшее время будут запущены другие полезные платные сервисы.

❓ Сколько нужно времени, чтобы найти идеальную пару для меня?

✅ Это зависит от наполненности базы в том регионе, где вы знакомитесь и от простого везения. В любом случае, при помощи нашего сервиса такая пара должна найтись гораздо быстрее, чем при помощи традиционных сервисов знакомств (Тиндер-модель и другие).''',
reply_markup=find_inline_keyboard)


@dp.callback_query_handler(text='investors')
async def show_investors(message: types.Message):
    investors_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='faq')
    investors_inline_keyboard.add(registration_button)
    investors_inline_keyboard.add(back_button)
    await bot.send_message(message.from_user.id, text='''❓ Я инвестор и хотел бы инвестировать.

✅ Свяжитесь напрямую с создателями системы Максимом Щегловым и Сергеем Сигитовым по адресу hello@unison.dating. Мы сообщим вам актуальную потребность в инвестициях и предпочтительные условия. Мы рассматриваем частные инвестиции и коммерческие фонды, специализирующиеся на b2с модели и прямой монетизации. 

По этому адресу нельзя получить помощь или сообщить о возврате денег. Все обращения подобной тематики необходимо отправлять в Службу поддержки.

❓ Как я могу связаться, чтобы получить франшизу или лицензию на использование системы в другой стране?

✅ Мы можем сотрудничать с локальными партнёрами в сфере интернет-маркетинга, пиара и различных форм продвижения интернет-проектов. Например, мы можем предоставлять приоритетное право на продвижение системы с помощью крупных локальных партнёров или приобрести возможность установки системы на телефоны производителей в пакете предустановленных программ. Пришлите ваше предложение по адресу hello@unison.dating''',
reply_markup=investors_inline_keyboard)


@dp.callback_query_handler(text='journalists')
async def show_journalists(message: types.Message):
    journalists_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='faq')
    journalists_inline_keyboard.add(registration_button)
    journalists_inline_keyboard.add(back_button)
    await bot.send_message(message.from_user.id, text='''❓ Я журналист и хочу попробовать систему, прежде чем писать про Unison. Что мне надо учесть?

✅ Так как у вас нет мотивации познакомиться, вы можете совершать много ошибок в процессе регистрации, и, скорее всего, будете заблокированы ранее, чем достигните первого результата.

Пожалуйста, обратите внимание, что для получения полного представления о системе вы должны быть твёрдо уверены, что хотите создать семью или начать отношения. Мы можем провести демонстрацию системы и предоставить данные статистики, если вы обратитесь по электронной почте hello@unison.dating''',
reply_markup=journalists_inline_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
