import json

from telebot import TeleBot
from telebot.types import Message, ChatMemberUpdated, CallbackQuery, ReplyKeyboardRemove
from catalogues.message_texts import MessageTexts
from config import BOT_ID, BASE_DIR
from keyboards.reply_keyboards import main_menu_keyboard
from models.users_model import Admin
from models.allowed_chats_model import AllowedGroup
from filters.chat_confirmation_filter import chat_template_data
from keyboards.bot_admin_keyboards import get_admin_confirmation


def command_start(message: Message, bot: TeleBot):
    bot.delete_my_commands()
    bot.set_my_commands(['start'])
    bot.send_message(message.chat.id, MessageTexts.START_MESSAGE,
                     reply_markup=main_menu_keyboard(),
                     parse_mode='markdown')

def command_clean_handler(message: Message, bot: TeleBot):
    bot.delete_my_commands()
    bot.send_message(message.chat.id, "очистка клавиатур в групповых чатах",
                     reply_markup=ReplyKeyboardRemove(),
                     parse_mode='markdown')


def command_my_id_handler(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, f"Ваш ID Telegram: `{message.chat.id}`",
                     reply_markup=ReplyKeyboardRemove(),
                     parse_mode='markdown')

def check_allowed_groups_handler(chat_member: ChatMemberUpdated, bot: TeleBot):
    # Проверяет на добавление бота в группу и направляет запрос подтверждения владельцу.
    if (BOT_ID == chat_member.new_chat_member.user.id
        and chat_member.new_chat_member.status != "left"):
        for i in Admin.ADMINS:
            bot.send_message(chat_id=i, text=f"Подтвердите добавление бота в группу\n"
                                             f"{chat_member.chat.id}:{chat_member.chat.title}",
                             reply_markup=get_admin_confirmation(chat_member.chat.id))

def chat_join_confrim_handler(call: CallbackQuery, bot: TeleBot):
    # Обрабатывает решение владельца бота на добавление в группу
    bot.answer_callback_query(call.id)
    callback_data: dict = chat_template_data.parse(callback_data=call.data)
    chat_id, param = int(callback_data["id"]), str(callback_data["param"])
    # print(chat_id, param)
    # Если владелец отклонил добавление - бот покидает чат
    if chat_id and param == "decline":
        bot.leave_chat(chat_id)
        bot.edit_message_text(MessageTexts.BOT_GROUP_DECLINE_MSG,
                              call.message.chat.id, call.message.id, reply_markup=None)
    else:
        # Иначе - помечает группу как разрешенную.
        bot.edit_message_text(MessageTexts.BOT_GROUP_CONFIRM_MSG,
                              call.message.chat.id, call.message.id, reply_markup=None)
        print(BASE_DIR)
        with open(str(BASE_DIR)+"/allowed_group.json", "w") as file:
            file.write(json.dumps({"group" : chat_id}))

def register_core_handlers(bot: TeleBot):
    bot.register_message_handler(command_start, commands=['start'], pass_bot=True, chat_types=['private'])
    bot.register_message_handler(command_my_id_handler, commands=['my_id'], pass_bot=True, chat_types=['private'])
    bot.register_message_handler(command_clean_handler, commands=['clean'], pass_bot=True, chat_types=['group'])
    bot.register_my_chat_member_handler(check_allowed_groups_handler, chat_types="group", pass_bot=True)
    bot.register_callback_query_handler(chat_join_confrim_handler, func=None,
                                        chat_confirm=chat_template_data.filter(), pass_bot=True)

