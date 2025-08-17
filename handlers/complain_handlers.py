from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from catalogues.message_texts import MessageTexts
from catalogues.button_texts import IssueButtons, ButtonTexts
from states.project_states import ComplainStates
from keyboards.reply_keyboards import (drink_not_provided_keyboard, drink_incorrect_keyboard,
                                       back_keyboard, confirm_keyboard, main_menu_keyboard)
from keyboards.staff_keyboards import get_staff_confirmation
from utils.bot_logger import logger
from models.allowed_chats_model import AllowedGroup


def drink_not_provided_handler(message: Message, bot: TeleBot):
    # Обработчик запросов по невыдаче напитка
    logger.debug("drink_not_provided_handler")
    bot.send_message(message.chat.id, text=MessageTexts.COMPLAIN_OFFER_MSG,
                     reply_markup=drink_not_provided_keyboard())

def wrong_drink_handler(message: Message, bot: TeleBot):
    # Обработчик обращений по некорректно приготовленным напиткам
    logger.debug("wrong_drink_handler")
    bot.send_message(message.chat.id, text=MessageTexts.COMPLAIN_OFFER_MSG,
                     reply_markup=drink_incorrect_keyboard())

def another_issue_type_handler(message: Message, bot: TeleBot):
    # Обработчик обращений по остальным проблемам
    logger.debug("another_issue_type_handler")
    bot.set_state(message.from_user.id, ComplainStates.issue_description_state, message.chat.id)
    bot.send_message(message.chat.id, text=MessageTexts.COMPLAIN_TEXT_REQUEST_MSG,
                     reply_markup=back_keyboard())

def issue_description_state_handler(message: Message, bot: TeleBot):
    # Обработчик полученного от пользователя описания по проблемам другого типа
    logger.debug("issue_description_state_handler")
    issue_text = message.text
    bot.add_data(message.from_user.id, message.chat.id, issue_text=issue_text)
    bot.send_message(message.chat.id, text=f"*Текст вашего запроса*:\n\"{issue_text}\"\n\n"
                                           f"Подтвердите отправку оператору.\n"
                                           f"*При подтверждении у вас будет запрошена информация о вашем "
                                           f"контакте для обратной связи с вами!*",
                     parse_mode='markdown',
                     reply_markup=confirm_keyboard())

def confirm_btn_handler(message: Message, bot: TeleBot):
    # Обработчик кнопки подтверждения отправки сообщения
    # !!!!! Переход к взаимодействию с техподдержкой
    logger.debug("confirm_btn_handler")
    # Отправляем данные в чат операторов для связи
    issue_text = bot.retrieve_data(message.from_user.id, message.chat.id).data['issue_text']

    bot.send_message(AllowedGroup.GROUP, MessageTexts.TECH_SUPPORT_MESSAGE.format(
        id=message.from_user.id, first_name=message.from_user.first_name,
        last_name=message.from_user.last_name, nickname=message.from_user.username,
        phone_number=message.contact.phone_number,
        reply_command=IssueButtons.ANOTHER_ISSUE_BTN, comment=issue_text
    ), reply_markup=ReplyKeyboardRemove(), parse_mode="markdown")
    # Отправляем сообщение пользователю
    bot.send_message(message.chat.id, MessageTexts.COMPLAIN_ACCEPT_MSG,
                     reply_markup=main_menu_keyboard())
    bot.delete_state(message.from_user.id, message.chat.id)

def cancel_btn_handler(message: Message, bot: TeleBot):
    # Обработчик кнопки отмены отправки сообщения
    logger.debug("cancel_btn_handler")
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, text=MessageTexts.RETURN_BTN_MESSAGE,
                     reply_markup=main_menu_keyboard())

def register_complain_handlers(bot: TeleBot):
    bot.register_message_handler(drink_not_provided_handler,
                                 is_button=IssueButtons.DRINK_NOT_PROVIDED_BNT,
                                 state=ComplainStates.dialogue_process_state,
                                 pass_bot=True)
    bot.register_message_handler(wrong_drink_handler,
                                 is_button=IssueButtons.WRONG_DRINK_BTN,
                                 state=ComplainStates.dialogue_process_state,
                                 pass_bot=True)
    bot.register_message_handler(another_issue_type_handler,
                                 is_button=IssueButtons.ANOTHER_ISSUE_BTN,
                                 state=ComplainStates.dialogue_process_state,
                                 pass_bot=True)
    bot.register_message_handler(confirm_btn_handler,
                                 content_types=['contact'],
                                 state=ComplainStates.issue_description_state,
                                 pass_bot=True)
    bot.register_message_handler(cancel_btn_handler,
                                 is_button=ButtonTexts.CANCEL_BTN,
                                 state=ComplainStates.issue_description_state,
                                 pass_bot=True)
    bot.register_message_handler(issue_description_state_handler,
                                 content_types=['text'],
                                 not_button=True,
                                 state=ComplainStates.issue_description_state,
                                 pass_bot=True)