from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="📝 Send scam", callback_data="send_scam"),
    InlineKeyboardButton(text="🔎 Check address", callback_data="check_address")],
    [InlineKeyboardButton(text="💰 Crypto cost", callback_data="cripto_cost")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Back to menu")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Back to menu", callback_data="menu")]])


crypto_list = [
    [InlineKeyboardButton(text="BTC-RUB", callback_data="BTC-RUB")],
    [InlineKeyboardButton(text="USDT-RUB", callback_data="USDT-RUB")]
]
crypto_list = InlineKeyboardMarkup(inline_keyboard=crypto_list)