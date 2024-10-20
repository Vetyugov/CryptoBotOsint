from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import flags
import logging
from db_service import DataBaseService
import cripto_osint_service
import text
import tg_key_boards
import cripto_cost_service
from states import CryptoState

router = Router()
db = DataBaseService(DataBaseService.SQLITE_FILE_PATH)

@router.message(Command("start"))
async def start_handler(msg: Message):
    logging.info("Поиск и сохранение пользователя")
    try:
        db.save_new_user(str(msg.from_user.id))
        logging.info("Успешно. Пользователь сохранен или уже существует")
    except Exception as e:
        logging.error('Произошла ошибка при сохранении пользователя', e)

    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=tg_key_boards.menu)

@router.message(F.text == "Меню")
@router.message(F.text == "Menu")
@router.message(F.text == "Back to menu")
@router.message(F.text == "◀️ Back to menu")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=tg_key_boards.menu)




# @router.message(F.text == "💰 Crypto cost")
# @router.message(F.text == "Crypto cost")
# @router.callback_query(F.data == "cripto_cost")
# async def choose_cripto_cost(msg: Message):
#     await msg.answer(text.choose_crypto, reply_markup=tg_key_boards.crypto_list)
#

@router.callback_query(F.data == "cripto_cost")
async def choose_cripto_cost(clbck: CallbackQuery):
    await clbck.message.answer(text.choose_crypto, reply_markup=tg_key_boards.crypto_list)


@router.callback_query(F.data == "BTC-RUB")
@router.callback_query(F.data == "USDT-RUB")
async def cripto_cost(clbck: CallbackQuery):
    cost_result = cripto_cost_service.cost(clbck.data)
    return clbck.message.answer(f'{clbck.data} : {cost_result.amount}, {cost_result.currency}', reply_markup=tg_key_boards.menu)


# @router.message(F.text == "🔎 Check address")
# @router.message(F.text == "Check address")
@router.callback_query(F.data == "check_address")
async def check_address(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(CryptoState.check_address)
    await clbck.message.answer(text.enter_crypto_address)
    await clbck.message.answer(text.dialog_exit, reply_markup=tg_key_boards.exit_kb)


@router.message(CryptoState.check_address)
@flags.chat_action("typing")
async def check_address_result(msg: Message, state: FSMContext):
    address = msg.text
    res = cripto_osint_service.check_address(address)
    if res is None:
        return msg.answer(text.request_error, reply_markup=tg_key_boards.iexit_kb)
    else:
        return msg.answer(res.get_desc(), reply_markup=tg_key_boards.menu)


# @router.callback_query(F.data == "send_scam")
# async def send_scam(clbck: CallbackQuery, state: FSMContext):
#     await state.set_state(CryptoState.check_address)
#     await clbck.message.edit_text(text.enter_crypto_address)
#     await clbck.message.answer(text.dialog_exit, reply_markup=tg_key_boards.exit_kb)



# @router.message(CryptoState.check_address)
# @flags.chat_action("typing")
# async def send_scam_result(msg: Message, state: FSMContext):
#     address = msg.text
#     res = cripto_osint_service.(address)
#     if res is None:
#         return msg.answer(text.request_error, reply_markup=tg_key_boards.iexit_kb)
#     else:
#         return msg.answer(res.get_desc, disable_web_page_preview=True)
