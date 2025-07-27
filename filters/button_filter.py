from telebot.types import CallbackQuery, Message
from telebot.custom_filters import AdvancedCustomFilter, SimpleCustomFilter
from catalogues.message_texts import MessageTexts

class IsButtonFilter(AdvancedCustomFilter):
    key = 'is_button'

    @staticmethod
    def check(message: Message, values):
        if message.content_type != 'text':
            return False
        return message.text in values


class NotAButtonFilter(SimpleCustomFilter):
    key = 'not_button'

    @staticmethod
    def check(message: Message):
        if message.content_type != 'text':
            return True
        return message.text not in MessageTexts.get_const_list()
