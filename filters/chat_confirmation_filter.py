from telebot.types import CallbackQuery
from telebot.custom_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter

chat_template_data = CallbackData("id", "param", prefix="chat")
refund_template_data = CallbackData("id", "param", prefix="refund")

class ChatConfirmCallbackFilter(AdvancedCustomFilter):
    key = 'chat_confirm'

    @staticmethod
    def check(call: CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class RefundConfirmCallbackFilter(AdvancedCustomFilter):
    key = 'refund_confirm'

    @staticmethod
    def check(call: CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)