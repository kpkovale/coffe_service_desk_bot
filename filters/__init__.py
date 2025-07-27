# register filters here or in different folders.
from .admin_filter import AdminFilter
from .button_filter import IsButtonFilter, NotAButtonFilter
from .chat_confirmation_filter import ChatConfirmCallbackFilter, RefundConfirmCallbackFilter
from telebot import TeleBot
from utils.bot_logger import logger
from config import LOG_LEVEL
from telebot.custom_filters import StateFilter


def register_filters(bot: TeleBot):
    logger.log(LOG_LEVEL, "Registering filters")

    bot.add_custom_filter(IsButtonFilter())
    bot.add_custom_filter(NotAButtonFilter())
    bot.add_custom_filter(AdminFilter())
    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(ChatConfirmCallbackFilter())
    bot.add_custom_filter(RefundConfirmCallbackFilter())

