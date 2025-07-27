from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from catalogues.button_texts import ButtonTexts, IssueButtons, SolutionButtons
from models.users_model import Admin


def main_menu_keyboard(add_button: str = None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(ButtonTexts.COMPLAIN_BTN),
               KeyboardButton(ButtonTexts.SUGGEST_BTN),
               KeyboardButton(ButtonTexts.PARTNERSHIP_BTN))
    if add_button:
        markup.add(KeyboardButton(add_button))
    return markup

def complain_menu_keyboard(add_button: str = None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(IssueButtons.DRINK_NOT_PROVIDED_BNT),
               KeyboardButton(IssueButtons.WRONG_DRINK_BTN),
               KeyboardButton(IssueButtons.ANOTHER_ISSUE_BTN),
               KeyboardButton(ButtonTexts.BACK_BTN))
    if add_button:
        markup.add(KeyboardButton(add_button))
    return markup

def drink_not_provided_keyboard(add_button: str = None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(SolutionButtons.REFUND_BTN),
               KeyboardButton(SolutionButtons.DONATION_BTN),
               KeyboardButton(SolutionButtons.STAFF_CONTACT_BTN),
               KeyboardButton(ButtonTexts.BACK_BTN))
    if add_button:
        markup.add(KeyboardButton(add_button))
    return markup

def drink_incorrect_keyboard(add_button: str = None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(SolutionButtons.REFUND_BTN),
               KeyboardButton(SolutionButtons.PARTLY_REFUND_BTN),
               KeyboardButton(SolutionButtons.STAFF_CONTACT_BTN),
               KeyboardButton(ButtonTexts.BACK_BTN))
    if add_button:
        markup.add(KeyboardButton(add_button))
    return markup

def request_contact(add_button: str = None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(ButtonTexts.REQUEST_CONTACT, request_contact=True))
    if add_button:
        markup.add(KeyboardButton(add_button))
    return markup

def back_keyboard(add_button: str = None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(ButtonTexts.BACK_BTN))
    if add_button:
        markup.add(KeyboardButton(add_button))
    return markup

def confirm_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(ButtonTexts.CONFIRM_BTN),
               KeyboardButton(ButtonTexts.CANCEL_BTN))
    return markup
