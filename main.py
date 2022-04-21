import telebot
from telebot import types

bot = telebot.TeleBot("5189585447:AAHdZcNKEvZsFfRApyLCdCV3kUqIUxa72ak")


@bot.message_handler(content_types="text")
def lisener(msg: types.Message):
    bot.send_message(msg.chat.id, f"Echo: {msg.text}")


@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


@bot.chosen_inline_handler(func=lambda result: True)
def test_chosen(result: types.ChosenInlineResult):
    if result.result_id == 1:
        bot.send_message(result.inline_message_id, "Result 1 bro")


bot.set_update_listener(lisener)
bot.infinity_polling()
