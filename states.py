from aiogram.fsm.state import StatesGroup, State

class CryptoState(StatesGroup):
    check_address = State()
    scam = State()
