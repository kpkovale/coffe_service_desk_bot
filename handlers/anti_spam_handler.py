from telebot import TeleBot
from telebot.types import Message
from keyboards.reply_keyboards import main_menu_keyboard
from catalogues.message_texts import MessageTexts
from utils.bot_logger import logger

def any_text_handler(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, MessageTexts.NO_BUTTONS_PRESSED_MSG,
                     reply_markup=main_menu_keyboard())
    logger.debug(bot.get_state(message.from_user.id, message.chat.id))