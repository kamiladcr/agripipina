from telebot import TeleBot
from telebot.types import Message

bot = TeleBot("6139726981:AAHYXuNByfotN4RFPkIoepNKrSaaSvyJJMg", parse_mode=None)


@bot.message_handler(commands=["help"])
def help(message):
	bot.reply_to(
		message,
		"hi. \nthis bot pins links so you can check them out later. \nuse the command /pin to specify which links you would like to pin \ne.g. /pin spotify soundcloud songwhip",
	)


@bot.message_handler(commands=["pin"])
def get_masks(message: Message):
	input = message.text if message.text else ""
	masks = input.split()[1:]
	print(f"masks: {masks}")
	text = "emply list" if message.text == "/pin" else "ok"
	sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
	bot.register_next_step_handler(sent_msg, process_masks)
	print(f"sent_msg: {sent_msg}")
	return message.text


def process_masks(message: Message) -> bool:
	entities = message.entities if message.entities else []
	for entity in entities:
		print(f"entity type: {entity.type}")
		if entity.type == "url":
			return True
	return False


@bot.message_handler(func=process_masks)
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
