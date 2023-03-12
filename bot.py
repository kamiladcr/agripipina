from telebot import TeleBot
from telebot.types import Message

bot = TeleBot("6139726981:AAHYXuNByfotN4RFPkIoepNKrSaaSvyJJMg", parse_mode=None)

# add dict with chat.id and masks
# persistence (add class with methods init, append, clear)

class State():
	def __init__(self):
		self.masks = []
	def append(self, value):
		self.masks.append(value)
	def clear(self):
		self.masks.clear()
	def __str__(self):
		masks = self.masks
		return "no masks" if masks == [] else "masks: " + str.join(", ", masks)



@bot.message_handler(commands=["help"])
def help(message):
	bot.reply_to(
		message,
		"""
		hi.
		this bot pins links so you can check them out later.
		use the command /pin to specify which links you would like to pin
		e.g. /pin spotify soundcloud
		add command to clear masks
		show to show all masks
		""",
	)


masks = State()

@bot.message_handler(commands=["show"])
def show_masks(message: Message):
	bot.send_message(message.chat.id, str(masks))


@bot.message_handler(commands=["pin"])
def add_masks(message: Message):
	user_input = message.text if message.text else ""
	for mask in user_input.split()[1:]:
		masks.append(mask)
	if message.text == "/pin":
		text = "usage: /pin spotify soundcloud"
		bot.send_message(message.chat.id, text)
	show_masks(message)


@bot.message_handler(commands=["clear"])
def clear_masks(message: Message):
	masks.clear()
	show_masks(message)


def process_masks(message: Message) -> bool:
	entities = message.entities if message.entities else []
	user_input = message.text if message.text else ""
	for entity in entities:
		text = user_input[entity.offset : entity.length]
		has_masks = any(map(lambda mask: mask in text, masks.masks))
		if entity.type == "url" and has_masks:
			return True
	return False


@bot.message_handler(func=process_masks)
def pin_message(message):
	bot.pin_chat_message(
		chat_id=message.chat.id,
		message_id=message.message_id,
		disable_notification=True,
	)


bot.infinity_polling()
