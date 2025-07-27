from telebot import TeleBot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from catalogues.message_texts import MessageTexts
from keyboards.reply_keyboards import main_menu_keyboard
from keyboards.staff_keyboards import get_staff_confirmation
from states.project_states import ComplainStates
from filters.chat_confirmation_filter import refund_template_data

def refund_confirm_handler(call: CallbackQuery, bot: TeleBot):
    # Обработчик подтверждения или отклонения возврата в чате техподдержки
    bot.answer_callback_query(call.id)
    callback_data: dict = refund_template_data.parse(callback_data=call.data)
    customer_chat_id, param = int(callback_data["id"]), str(callback_data["param"])
    upd_staff_msg_text = (call.message.text +
                          MessageTexts.STAFF_REFUND_CONFIRMED_MSG.format(call.from_user.username))
    upd_customer_msg_text = MessageTexts.REFUND_CONFIRMED_MSG
    if param == "decline":
        upd_staff_msg_text = (call.message.text +
                              MessageTexts.STAFF_REFUND_DECLINED_MSG.format(call.from_user.username))
        upd_customer_msg_text = MessageTexts.REFUND_DECLINED_MSG

    bot.edit_message_text(text=upd_staff_msg_text,
                              chat_id=call.message.chat.id, message_id=call.message.id,
                              parse_mode='markdown', reply_markup=None)
    bot.send_message(customer_chat_id, upd_customer_msg_text, reply_markup=main_menu_keyboard(),
                     parse_mode='markdown')

def register_refund_action_handlers(bot: TeleBot):
    bot.register_callback_query_handler(refund_confirm_handler, func=None,
                                        refund_confirm=refund_template_data.filter(), pass_bot=True)
    bot.register_callback_query_handler(refund_confirm_handler, func=None,
                                        refund_confirm=refund_template_data.filter(), pass_bot=True)
