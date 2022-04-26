import telebot
from telebot.types import *
from random import randint
from classes import *

sessions = []
bot = telebot.TeleBot("5189585447:AAHdZcNKEvZsFfRApyLCdCV3kUqIUxa72ak")


@bot.message_handler(commands=["session"], chat_types=["group"])
def create_session(msg: Message):
    # Get all sessions in current chat.
    session_amount = get_chat_sessions(msg.chat.id)
    #
    if session_amount is not None:
        session_amount = len(get_chat_sessions(msg.chat.id))
    new_session_id = get_new_id()
    sessions.append(Session(identification=new_session_id, chat=msg.chat.id))
    bot.send_message(msg.chat.id, f"Игра создана под номером {new_session_id} . Используйте команду /join чтобы присоединиться к комнате.")


@bot.message_handler(commands=["join"], chat_types=["group"])
def join_session(msg: Message):
    # Get all sessions in current chat.
    chat_session = get_chat_sessions(msg.chat.id)
    # Сообщение в случае когда нету игр
    if chat_session is None:
        bot.send_message(msg.chat.id, f"@{msg.from_user.username} ни одной игры еще не было создано. Для создания игры напишите /session.")
        return
    # Разметка для конопок
    join_markup = InlineKeyboardMarkup(row_width=2)
    # Для каждой сессии этого чата, делает кнопку.
    for session in chat_session:
        session_id = session.id
        join_markup.add(InlineKeyboardButton(text=f"Игра: {session_id}. Игроков {len(session)}/2",
                                             callback_data=f"join:{session_id}"))
    # Отсылаем сообщение с выбором сессий.
    bot.send_message(msg.chat.id, f"@{msg.from_user.username} выберете игру.", reply_markup=join_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("join:"))
def join_request(call: CallbackQuery):
    # Так как входящий запрос всегда будет с join: , просто отрезаем его от числа и конвертуруем в число.
    session_id = int(call.data.split(sep="join:")[1])

    callback_chat_id = call.message.chat.id
    callback_user = call.from_user
    # Get all sessions in callback's chat.
    chat_session = get_chat_sessions(callback_chat_id)

    # Проверяем на наличие игрока в сессии
    for session in chat_session:
        # Проверяем если ли в этой комнате пользователь
        for player in session.get_players():
            if player.this_user(user_id=callback_user.id):
                bot.send_message(callback_chat_id, f"@{callback_user.username} вы уже учасник комнаты {session.id}")
                return

    # Сравниваем все комнаты в чате, с нужной нам комнатой.
    for session in chat_session:

        if session.id == session_id:
            # Проверяем заполнена ли сессия
            if len(session) >= 2:
                bot.send_message(callback_chat_id, f"@{callback_user.username} игра уже заполнена.")
                return

            # Добавляем игрока в сессию (Нужно еще потом делать проверки, что игрок уже зашел в комнату, и не может зайти в другие)
            session.add_players(Player(user_id=callback_user.id))
            # Удаляем сообщение с выбором комнат.
            bot.delete_message(chat_id=callback_chat_id, message_id=call.message.message_id)
            # Говорим пользователю, что он присоидинился.
            bot.send_message(callback_chat_id, f"@{callback_user.username} вы присоидинились в комнату {session_id}")
            return
    # Либо говорим что что-то пошло не так.
    bot.send_message(callback_chat_id, f"@{callback_user.username} Что-то пошло не так.")


@bot.message_handler(commands="value")
def get_value_player(msg: Message):
    bot.send_message(msg.chat.id, "Напишите номер сессии")



def get_chat_sessions(chat: int):
    """
    Return all sessions created in this chat.
    :param chat:  Chat where you look for sessions.
    :return: False если их нет. Либо последнию сессию.
    """
    chat_sessions = []
    for session in sessions:
        if session.chat_id == chat:
            chat_sessions.append(session)
    if len(chat_sessions) <= 0:
        return None
    return chat_sessions


def get_new_id():
    used_ids = []
    for session in sessions:
        used_ids.append(session.id)
    id = 0
    while id == 0:
        for i in range(0, 4):
            id += randint(1, 9) * pow(10, i)
        if id in used_ids:
            id = 0
    return id


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()
