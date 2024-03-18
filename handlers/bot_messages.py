from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from keyboards.reply import main, ispravit
from aiogram.fsm.context import FSMContext
from utils.stateforms import StepsForm
from keyboards.inline import inline_kb
# from handlers.user_messages import g
from id import a
import os
import dotenv
import zipfile

dotenv.load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode='HTML')

channel_id = -1002084616413

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    if message.chat.id != channel_id:
        await message.answer(f"Привет, {message.from_user.first_name}! Чтобы начать наше общение, нажмите на кнопочку", reply_markup=main)
    else:
        pass

# async def cmd_start(message: Message):
#     if message.text.lower() == 'qwerty123':
#         await message.answer('Нажми на кнопку', reply_markup=main)
#     else:
#         await message.answer("неправильный пароль")

@router.message(Command("help"))
async def cmd_start(message: Message):
    await message.answer('Список команд:\n/start - начать общение\n/help - список команд\n/form - начать заполнение заявки\nЕсли у вас появились какие-то проблемы, то пишите вот этому другу, https://vk.com/m0kas1')
@router.message()
async def get_start(message: Message, state: FSMContext):
    if (message.text.lower() == 'отправить проблему' or message.text.lower() == '/form') and message.chat.id != channel_id:
        # await message.answer(f'Твоё ФИО: {message.text}')
        # await message.answer('Выберите ваш завод', reply_markup=inline.inline_kb)
        await message.answer('Выберите ваш завод', reply_markup=inline_kb.as_markup())
        await state.set_state(StepsForm.GET_CHEH)
    # if message.text.lower() == 'отправить проблему' or message.text.lower() == '/form':
    #     await message.answer('Введите ваше ФИО')
    #     await state.set_state(StepsForm.GET_FIO)
    # else:
    #     await message.answer('Нажми на кнопочку ↓', reply_markup=main)
@router.callback_query(F.data.startswith("«"))
async def get_CHEH(callback: CallbackQuery, state: FSMContext):
    # if message.text.count(' ') == 2 and message.text.count(' ') != len(message.text):
    #     # await message.answer(f'Твоё ФИО: {message.text}')
    #     await state.update_data(fio=message.text)
    #     await state.set_state(StepsForm.GET_CHEH)
    #     # await message.answer('Выберите ваш завод', reply_markup=inline.inline_kb)
    #     await message.answer('Выберите ваш завод', reply_markup=inline_kb.as_markup())
    # else:
    #     await message.answer('Попробуйте ещё раз')
    try:
        await state.update_data(cheh=callback.data)
        await state.set_state(StepsForm.GET_FIO)
        await callback.message.answer('Введите ваше ФИО')
    except AttributeError:
        pass
async def get_FIO(message: Message, state: FSMContext):
    if message.text.count(' ') == 2 and message.text.count(' ') != len(message.text):
        await state.update_data(fio=message.text)
        await state.set_state(StepsForm.GET_PODRASDELENIE)
        await message.answer('Введите ваше подразделение:')
    else:
        await message.answer('Попробуйте ещё раз')
    # await state.update_data(fio=message.text)
    # await state.set_state(StepsForm.GET_PODRASDELENIE)
    # await callback.message.answer('Введите ваше подразделение:')
# async def get_CHEH(message: Message, state: FSMContext):
#     # await message.answer(f'Ваш СП: {message.text}')
#     await state.update_data(cheh=message.text)
#     await state.set_state(StepsForm.GET_PODRASDELENIE)
#     await message.answer('Введите ваше подразделение:')

async def get_PODRASDELENIE(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer('Введите нормально текст')
    # await message.answer(f'Ваше подразделение: {message.text}')
    else:
        await state.update_data(podraselenit=message.text)
        await state.set_state(StepsForm.GET_ULUCHENIE)
        await message.answer('Укажите область улучшения:\n(Безопастность, качество, производительность, эргономика',)

async def get_ULUCHENIE(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer('Введите нормально текст')
    # await message.answer(f'Ваше подразделение: {message.text}')
    else:
        await state.update_data(uluchenie=message.text)
        await state.set_state(StepsForm.GET_PREDLOSHENIE)
        await message.answer('Напишите название предложения:')

async def get_PREDLOSHENIE(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer('Введите нормально текст')
    # await message.answer(f'Ваше подразделение: {message.text}')
    else:
        await state.update_data(predloshenie=message.text)
        await state.set_state(StepsForm.GET_PROBLEMA)
        await message.answer('Опишите вашу проблему')
async def get_PROBLEMA(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer('Введите нормально текст')
    else:
        await state.update_data(problema=message.text)
        await state.set_state(StepsForm.GET_PHOTO_1)
        await message.answer('Отправьте фото. ЕСЛИ ФОТО НЕТ - ВВЕДИТЕ ЛЮБОЙ ТЕКСТ')

async def get_PHOTO_1(message: Message, state: FSMContext, bot: Bot):
    # global data_user, PHOTO, TEG
    # await state.update_data(photo=message.photo[-1].file_id)
    # await state.set_state(StepsForm.GET_PHOTO)
    c = 0
    while c != 1:
        if message.photo:
            await state.update_data(photo_1=message.photo[-1].file_id)
            await state.set_state(StepsForm.GET_PHOTO_1)
            await bot.download(
                message.photo[-1],
                destination=f"img/{message.photo[-1].file_id}.jpg"
            )
            await state.set_state(StepsForm.GET_RESHENIE)
            await message.answer('Опишите ваше решение проблемы:')
            c = 1
        else:
            # d = message.text.lower()
            # if d == 'нет':
            #     c = 1
            #     break
            # else:
            # await message.answer('Введите корректное значение')
            await state.set_state(StepsForm.GET_RESHENIE)
            await message.answer('Опишите ваше решение проблемы:')
            break


async def get_RESHENIE(message: Message, state: FSMContext):
    if message.text == None:
        await message.answer('Введите нормально текст')
    else:
        await state.update_data(reshenie=message.text)
        await state.set_state(StepsForm.GET_PHOTO_2)
        await message.answer('Отправьте фото. ЕСЛИ ФОТО НЕТ - ВВЕДИТЕ ЛЮБОЙ ТЕКСТ')

async def get_PHOTO_2(message: Message, state: FSMContext, bot: Bot):
    global data_user, PHOTO_1, TEG, PHOTO_2
    # await state.update_data(photo=message.photo[-1].file_id)
    # await state.set_state(StepsForm.GET_PHOTO)
    c = 0
    while c != 1:
        if message.photo:
            await state.update_data(photo_2=message.photo[-1].file_id)
            await state.set_state(StepsForm.GET_PHOTO_2)
            await bot.download(
                message.photo[-1],
                destination=f"img/{message.photo[-1].file_id}.jpg"
            )
            c = 1
        else:
            # d = message.text.lower()
            # if d == 'нет':
            #     c = 1
            #     break
            # else:
            # await message.answer('Введите корректное значение')
            break

    content_data = await state.get_data()
    TEG = f'@{message.from_user.username}'
    d = dict(content_data)
    # print(content_data.__dict__)
    d['TEG'] = TEG
    print(f'Данные отправителя {d}')
    # print(d['photo'][-1])
    FIO = content_data.get('fio')
    CHEH = content_data.get('cheh')
    PODRASDELENIE = content_data.get('podraselenit')
    ULUCHENIE = content_data.get('uluchenie')
    PREDLOSHENIE = content_data.get('predloshenie')
    RESHENIE = content_data.get('reshenie')
    PROBLEMA = content_data.get('problema')
    PHOTO_1 = content_data.get('photo_1')
    PHOTO_2 = content_data.get('photo_2')
    data_user = f'Данные пользователя:\r\n\n' \
                f'ФИО: {FIO}\n' \
                f'Место работы: {CHEH}\n' \
                f'Подразделение: {PODRASDELENIE}\n' \
                f'Область улучшения: {ULUCHENIE}\n' \
                f'Предложение: {PREDLOSHENIE}\n' \
                f'Проблема: {PROBLEMA}\n' \
                f'Решение: {RESHENIE}\n' \
                f'Тег: {TEG}'
    # await message.answer(data_user)
    if PHOTO_1 is None and PHOTO_2 is None:
        await message.answer(data_user)
        await message.answer('Всё верно?', reply_markup=ispravit)
    else:
        if PHOTO_1 is None:
            g_2 = InputMediaPhoto(type='photo', media=FSInputFile(f'img/{PHOTO_2}.jpg'), caption=data_user)
            media = [g_2]
            await message.answer_media_group(media)
            await message.answer('Всё верно?', reply_markup=ispravit)
        # await message.answer_photo(photo=PHOTO_1)
        # await message.answer_photo(photo=PHOTO_2, caption=data_user, reply_markup=ispravit)
        else:
            if PHOTO_2 is None:
                g_1 = InputMediaPhoto(type='photo', media=FSInputFile(f'img/{PHOTO_1}.jpg'), caption=data_user)
                media = [g_1]
                await message.answer_media_group(media)
                await message.answer('Всё верно?', reply_markup=ispravit)
            else:
                g_1 = InputMediaPhoto(type='photo', media=FSInputFile(f'img/{PHOTO_1}.jpg'))
                g_2 = InputMediaPhoto(type='photo', media=FSInputFile(f'img/{PHOTO_2}.jpg'), caption=data_user)
                media = [g_1, g_2]
                await message.answer_media_group(media)
                await message.answer('Всё верно?', reply_markup=ispravit)
    await state.update_data(gey=message.text)
    await state.set_state(StepsForm.GET_vibor)

async def get_VIBER(message: Message, state: FSMContext):
    if message.text.lower() == 'исправить':
        await state.clear()
        if os.path.isfile(f'img/{PHOTO_1}.jpg') or os.path.isfile(f'img/{PHOTO_2}.jpg'):
            os.remove(f'img/{PHOTO_1}.jpg')
            os.remove(f'img/{PHOTO_2}.jpg')

        if os.path.isfile(f'txt/{TEG}.txt'):
            os.remove(f'txt/{TEG}.txt')

        if os.path.isfile(f'zip/{TEG}.zip'):
            os.remove(f'zip/{TEG}.zip')
        # removing_files = glob.glob(f'/img/{PHOTO}.jpg')
        # for i in removing_files:
        #     os.remove(i)
        await message.answer(f"Давай ещё раз, только будь аккуратнее! Незабудь нажать на кнопку ниже 👇", reply_markup=main)
        # await message.answer(get_start)
    if message.text.lower() == 'отправить':
        await state.clear()
        my_file = open(f"txt/{TEG}.txt", "w+", encoding='utf-8')
        my_file.write(data_user)
        my_file.close()

        file_zip = zipfile.ZipFile(f'zip/{TEG}.zip', 'w')
        file_zip.close()

        file_zip = zipfile.ZipFile(f'zip/{TEG}.zip', 'a')
        file_zip.write(f'txt/{TEG}.txt')
        # if os.path.isfile(f'img/{PHOTO_1}.jpg') is None and os.path.isfile(f'img/{PHOTO_2}.jpg') is None:
        if PHOTO_1 is None and PHOTO_2 is None:
            pass
            # file_zip.write(f'img/{PHOTO_1}.jpg')
            # file_zip.write(f'img/{PHOTO_2}.jpg')
        else:
            # if os.path.isfile(f'img/{PHOTO_1}.jpg') is None:
            if PHOTO_1 is None:
                file_zip.write(f'img/{PHOTO_2}.jpg')
            # elif os.path.isfile(f'img/{PHOTO_2}.jpg') is None:
            elif PHOTO_2 is None:
                file_zip.write(f'img/{PHOTO_1}.jpg')
            else:
                file_zip.write(f'img/{PHOTO_1}.jpg')
                file_zip.write(f'img/{PHOTO_2}.jpg')
        file_zip.close()

        documnet = FSInputFile(path=f'zip/{TEG}.zip')
        await message.answer('Файл отправлен!!!', reply_markup=main)
        # await message.answer_document(document=documnet, caption='Открой меня)')
        await bot.send_document(chat_id=channel_id, document=documnet)
        # await message.copy_to(chat_id=channel_id, caption=j.message_id)

        # if os.path.isfile(f'img/{PHOTO_1}.jpg') is None and os.path.isfile(f'img/{PHOTO_2}.jpg') is None:
        if PHOTO_1 is None and PHOTO_2 is None:
            # os.remove(f'img/{PHOTO_1}.jpg')
            # os.remove(f'img/{PHOTO_2}.jpg')
            pass
        else:
            # if os.path.isfile(f'img/{PHOTO_1}.jpg') is None:
            if PHOTO_1 is None:
                os.remove(f'img/{PHOTO_2}.jpg')
            # elif os.path.isfile(f'img/{PHOTO_2}.jpg') is None:
            elif PHOTO_2 is None:
                os.remove(f'img/{PHOTO_1}.jpg')
            else:
                os.remove(f'img/{PHOTO_1}.jpg')
                os.remove(f'img/{PHOTO_2}.jpg')

        if os.path.isfile(f'txt/{TEG}.txt'):
            os.remove(f'txt/{TEG}.txt')

        if os.path.isfile(f'zip/{TEG}.zip'):
            os.remove(f'zip/{TEG}.zip')
        # b = {"photo": PHOTO, "caption": data_user}
        # await message.forward_from_message_id()
        # await state.clear()
        # if PHOTO is None:
        #     # await message.answer(chat_id=, text=data_user)
        #     await message.answer(chat_id="6383652769", text=data_user)