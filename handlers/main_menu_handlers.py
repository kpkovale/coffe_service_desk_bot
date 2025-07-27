from telebot import TeleBot
from telebot.types import Message
from catalogues.message_texts import MessageTexts
from catalogues.button_texts import IssueButtons, ButtonTexts
from keyboards.reply_keyboards import (main_menu_keyboard, complain_menu_keyboard,
                                       request_contact, back_keyboard)
from states.project_states import ComplainStates
from models.allowed_chats_model import AllowedGroup
from utils.bot_logger import logger


def complain_bnt_handler(message: Message, bot: TeleBot):
    # Обработчик нажатия кнопки "У меня есть проблема"
    logger.debug("complain_bnt_handler")
    bot.set_state(message.from_user.id, ComplainStates.dialogue_process_state,
                  message.chat.id)
    bot.send_message(chat_id=message.chat.id,
                     text=MessageTexts.MAIN_COMPLAIN_MESSAGE,
                     reply_markup=complain_menu_keyboard())

def suggest_bnt_handler(message: Message, bot: TeleBot):
    # Обработчик нажатия кнопки "У меня есть предложение"
    logger.debug("suggest_bnt_handler")
    bot.set_state(message.from_user.id, ComplainStates.suggestion_state,
                  message.chat.id)
    bot.send_message(chat_id=message.chat.id,
                     text=MessageTexts.MAIN_SUGGESTION_MSG,
                     reply_markup=back_keyboard())

def suggest_text_handler(message: Message, bot: TeleBot):
    logger.debug("suggest_text_handler")
    # Обработчик текста с предложением от пользователя
    bot.delete_state(message.from_user.id, message.chat.id)
    # Отправляем сообщение пользователю
    bot.send_message(message.chat.id, MessageTexts.FEEDBACK_ACCEPT_MSG, reply_markup=main_menu_keyboard())
    # Отправляем сообщение операторам
    bot.send_message(AllowedGroup.GROUP, MessageTexts.USER_SUGGEST_MSG,
                     reply_markup=None)
    bot.forward_message(AllowedGroup.GROUP, message.chat.id, message.id)


def partnership_bnt_handler(message: Message, bot: TeleBot):
    # Обработчик нажатия кнопки "Мне интересно сотрудничество"
    logger.debug("partnership_bnt_handler")
    bot.set_state(message.from_user.id, ComplainStates.dialogue_process_state,
                  message.chat.id)
    bot.send_message(chat_id=message.chat.id,
                     text=MessageTexts.REQUEST_CONTACT_MSG,
                     reply_markup=request_contact(ButtonTexts.BACK_BTN))

def partnership_contact_accept_handler(message: Message, bot: TeleBot):
    # Обработчик полученного контакта по запросу партнёрки
    logger.debug("partnership_contact_accept_handler")
    bot.send_message(message.chat.id, MessageTexts.THANK_YOU_MSG, main_menu_keyboard())
    bot.send_message(AllowedGroup.GROUP, text=MessageTexts.PARTNERSHIP_NOTIFY_MSG)
    bot.forward_message(AllowedGroup.GROUP, message.chat.id, message.id)


def return_btn_handler(message: Message, bot: TeleBot):
    # Обработчик нажатия кнопки "⬅" (воврат в основное меню)
    logger.debug("return_btn_handler")
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, text=MessageTexts.RETURN_BTN_MESSAGE,
                     reply_markup=main_menu_keyboard())

def register_main_menu_handlers(bot: TeleBot):
    bot.register_message_handler(complain_bnt_handler, is_button=ButtonTexts.COMPLAIN_BTN,
                                 pass_bot=True, chat_types=['private'])
    bot.register_message_handler(suggest_bnt_handler, is_button=ButtonTexts.SUGGEST_BTN,
                                 pass_bot=True, chat_types=['private'])
    bot.register_message_handler(partnership_bnt_handler, is_button=ButtonTexts.PARTNERSHIP_BTN,
                                 pass_bot=True, chat_types=['private'])
    bot.register_message_handler(return_btn_handler, is_button=ButtonTexts.BACK_BTN,
                                 pass_bot=True, chat_types=['private'])
    bot.register_message_handler(suggest_text_handler, content_types=['text'],
                                 state=ComplainStates.suggestion_state,
                                 not_button=True,
                                 pass_bot=True, chat_types=['private'])
    bot.register_message_handler(partnership_contact_accept_handler, content_types=['contact'],
                                 state=ComplainStates.dialogue_process_state,
                                 pass_bot=True, chat_types=['private'])

