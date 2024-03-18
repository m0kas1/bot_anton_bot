from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

inline_kb = InlineKeyboardBuilder()
inline_kb.button(text='«ЮМЭК»', callback_data='«ЮМЭК»')
inline_kb.button(text='«МЗВА-ЧЭМЗ»', callback_data='«МЗВА-ЧЭМЗ»')
inline_kb.button(text='«ИНСТА»', callback_data='«ИНСТА»')
inline_kb.button(text='«Энерготрансизолятор»', callback_data='«Энерготрансизолятор»')
inline_kb.button(text='«ВОЛЬТА»', callback_data='«ВОЛЬТА»')
inline_kb.button(text='«ФОРЭНЕРГО-ИНЖИНИРИНГ»', callback_data='«ФОРЭНЕРГО-ИНЖИНИРИНГ»')
inline_kb.button(text='«ВОЛСКОМ»', callback_data='«ВОЛСКОМ»')
inline_kb.button(text='«ЮЗРК ГРУПП»', callback_data='«ЮЗРК ГРУПП»')
inline_kb.adjust(2)


