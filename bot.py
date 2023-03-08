from telebot import TeleBot
from telebot.types import Message

bot = TeleBot("6139726981:AAHYXuNByfotN4RFPkIoepNKrSaaSvyJJMg", parse_mode=None)


@bot.message_handler(commands=["help"])
def help(message):
	bot.reply_to(message, "hei, handsome. this bot pins music links...")


@bot.message_handler(commands=["pin"])
def what_links(message: Message):
	text = "what would you like to pin?"
	sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
	bot.register_next_step_handler(sent_msg, to_pin)


# @bot.message_handler(commands=["pin"])
# def send_welcome(message: Message):
#	bot.reply_to(message, "what to pin")


def to_pin(message: Message) -> bool:
	entities = message.entities if message.entities else []
	for entity in entities:
		if entity.type == "url":
			return True
	return False


@bot.message_handler(func=to_pin)
def pin_message(message):
	bot.pin_chat_message(
		chat_id=message.chat.id,
		message_id=message.message_id,
		disable_notification=True,
	)


# @bot.message_handler(content_types=['sticker'])
# def reply_to_sticker(message):
#         bot.reply_to(message, "oh your silly stickers again")


bot.infinity_polling()
