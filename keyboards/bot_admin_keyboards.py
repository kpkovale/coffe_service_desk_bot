from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from catalogues.button_texts import ButtonTexts
from filters.chat_confirmation_filter import chat_template_data

def get_admin_confirmation(chat_id: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=ButtonTexts.CONFIRM_BTN,
                                    callback_data=chat_template_data.new(id=chat_id, param="confirm")))
    markup.add(InlineKeyboardButton(text=ButtonTexts.CANCEL_BTN,
                                    callback_data=chat_template_data.new(id=chat_id, param="decline")))
    return markup
