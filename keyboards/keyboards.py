from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, BotCommand, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import Bot
from config.config import load_config


def create_inline_keyboard(width, *args, **kwargs):
    kb_builder = InlineKeyboardBuilder()
    buttons = []

    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(text=button,
                                     callback_data=button)
            )

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(
                InlineKeyboardButton(text=text,
                                     callback_data=button)
            )

    kb_builder.row(width=width, *buttons)
    return kb_builder.as_markup()


def create_reply_keyboard(width, *args):
    kb_builder = ReplyKeyboardBuilder()
    buttons = []

    if args:
        for text in args:
            buttons.append(
                KeyboardButton(text=text)
            )

    kb_builder.row(width=width, *buttons)
    return kb_builder.as_markup(resize_keyboard=True)


head_reply_keyboard = create_reply_keyboard(2,
                                            "🔖 Сегодня", "🔜 Завтра",
                                            "📅 Расписание по датам","📝 Расписание на неделю")


