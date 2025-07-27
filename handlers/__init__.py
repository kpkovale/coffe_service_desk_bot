# Create files for handlers in this folder.
from telebot import TeleBot

from .anti_spam_handler import any_text_handler
from .core_handlers import register_core_handlers
from .main_menu_handlers import register_main_menu_handlers
from .complain_handlers import register_complain_handlers
from .purchase_complain_handlers import register_purchase_complain_handlers
from .refund_action_handlers import register_refund_action_handlers
from utils.bot_logger import logger
from config import LOG_LEVEL


def register_handlers(bot: TeleBot):
    logger.log(LOG_LEVEL, "Registering handlers.")

    register_core_handlers(bot)
    register_main_menu_handlers(bot)
    register_complain_handlers(bot)
    register_purchase_complain_handlers(bot)
    register_refund_action_handlers(bot)

    bot.register_message_handler(any_text_handler, content_types=['text'], state=None,
                                 pass_bot=True, chat_types=['private'])