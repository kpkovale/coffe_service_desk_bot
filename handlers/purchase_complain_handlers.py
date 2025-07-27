from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from catalogues.message_texts import MessageTexts
from catalogues.button_texts import IssueButtons, ButtonTexts, SolutionButtons
from models.allowed_chats_model import AllowedGroup
from states.project_states import ComplainStates
from keyboards.reply_keyboards import (back_keyboard, confirm_keyboard,
                                       main_menu_keyboard, request_contact)
from keyboards.staff_keyboards import get_staff_confirmation
from utils.bot_logger import logger

def refund_request_handler(message: Message, bot: TeleBot):
    # Обработчик запроса на возврат средств
    bot.set_state(message.from_user.id, ComplainStates.full_refund_state, message.chat.id)
    bot.send_message(message.chat.id, text=MessageTexts.REFUND_REQUEST_MSG,
                     reply_markup=back_keyboard(),
                     parse_mode="markdown")

def partial_refund_request_handler(message: Message, bot: TeleBot):
    # Обработчик запроса на частичный возврат средств
    bot.set_state(message.from_user.id, ComplainStates.part_refund_state, message.chat.id)
    bot.send_message(message.chat.id, text=MessageTexts.PART_REFUND_REQ_MSG,
                     reply_markup=back_keyboard(),
                     parse_mode="markdown")

def refund_data_handler(message: Message, bot: TeleBot):
    # Обработчик сообщения с датой и предметом покупки для возврата средств
    bot.add_data(user_id=message.from_user.id, chat_id=message.chat.id,
                 refund_text=message.text)
    bot.send_message(message.chat.id, text=MessageTexts.REQUEST_CONTACT_MSG,
                     reply_markup=request_contact(ButtonTexts.BACK_BTN))

def donation_request_handler(message: Message, bot: TeleBot):
    # Обработчик запроса на донат вместо воврата. УРА!
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, text=MessageTexts.DONATION_MSG,
                     reply_markup=main_menu_keyboard())

def staff_contact_request_handler(message: Message, bot: TeleBot):
    # Обработчик запроса на cвязь пользователя с оператором
    bot.set_state(message.from_user.id, ComplainStates.contact_staff_state, message.chat.id)
    bot.send_message(message.chat.id, text=MessageTexts.REQUEST_CONTACT_MSG,
                     reply_markup=request_contact(ButtonTexts.BACK_BTN))

def complain_contact_shared_handler(message: Message, bot: TeleBot):
    # Обработчик полученного контакта и его отправки в группу тех поддержки
    logger.debug('enter complain_contact_shared_handler')
    state = bot.get_state(message.from_user.id, message.chat.id)
    state = ComplainStates.__dict__[state[state.find(":")+1:]]
    data: dict = bot.retrieve_data(message.from_user.id, message.chat.id).data
    if 'refund_text' in data.keys():
        refund_text = data['refund_text']
    else: refund_text = ""
    staff_keyboard = ReplyKeyboardRemove()
    if state in (ComplainStates.full_refund_state, ComplainStates.part_refund_state):
        staff_keyboard = get_staff_confirmation(message.chat.id)

    if state == ComplainStates.full_refund_state:
        reply_command = SolutionButtons.REFUND_BTN
    else:
        if state == ComplainStates.part_refund_state:
            reply_command = SolutionButtons.PARTLY_REFUND_BTN
        else : reply_command = SolutionButtons.STAFF_CONTACT_BTN

    #Отправляем данные в чат операторов для связи
    bot.send_message(AllowedGroup.GROUP, MessageTexts.TECH_SUPPORT_MESSAGE.format(
        id=message.chat.id, first_name=message.from_user.first_name,
        last_name=message.from_user.last_name, nickname=message.from_user.username,
        phone_number=message.contact.phone_number,
        reply_command=reply_command, comment=refund_text
    ), reply_markup=staff_keyboard, parse_mode="markdown")
    # Отправляем сообщение пользователю
    bot.send_message(message.chat.id, MessageTexts.COMPLAIN_ACCEPT_MSG,
                     reply_markup=main_menu_keyboard())
    bot.delete_state(message.from_user.id, message.chat.id)

def register_purchase_complain_handlers(bot: TeleBot):
    bot.register_message_handler(refund_request_handler,
                                 is_button=SolutionButtons.REFUND_BTN,
                                 state=ComplainStates.dialogue_process_state,
                                 pass_bot=True)

    bot.register_message_handler(partial_refund_request_handler,
                                 is_button=SolutionButtons.PARTLY_REFUND_BTN,
                                 state=ComplainStates.dialogue_process_state,
                                 pass_bot=True)

    bot.register_message_handler(donation_request_handler,
                                 is_button=SolutionButtons.DONATION_BTN,
                                 state=ComplainStates.dialogue_process_state,
                                 pass_bot=True)

    bot.register_message_handler(staff_contact_request_handler,
                                 is_button=SolutionButtons.STAFF_CONTACT_BTN,
                                 state=ComplainStates.dialogue_process_state,
                                 pass_bot=True)

    bot.register_message_handler(refund_data_handler,
                                 content_types=['text'],
                                 not_button=True,
                                 state=ComplainStates.full_refund_state,
                                 pass_bot=True)

    bot.register_message_handler(refund_data_handler,
                                 content_types=['text'],
                                 not_button=True,
                                 state=ComplainStates.part_refund_state,
                                 pass_bot=True)

    bot.register_message_handler(complain_contact_shared_handler,
                                 content_types=['contact'],
                                 state=ComplainStates.full_refund_state,
                                 pass_bot=True)

    bot.register_message_handler(complain_contact_shared_handler,
                                 content_types=['contact'],
                                 state=ComplainStates.part_refund_state,
                                 pass_bot=True)

    bot.register_message_handler(complain_contact_shared_handler,
                                 content_types=['contact'],
                                 state=ComplainStates.contact_staff_state,
                                 pass_bot=True)
