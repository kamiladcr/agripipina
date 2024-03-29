from telebot import TeleBot
from telebot.types import Message
import json
import os

token = os.environ["TOKEN"]
bot = TeleBot(token, parse_mode=None)
print(f"token: {token}")

state_file = "state/chat_state.json"
os.makedirs("state", exist_ok=True)


class State:
	def __init__(self):
		try:
			with open(state_file, "r") as read_file:
				data = read_file.read()
				self.chat_state = json.loads(data)
		except Exception:
			self.chat_state = {}

	def append(self, chat_id: str, value: str) -> None:
		if chat_id in self.chat_state:
			self.chat_state[chat_id].append(value)
		else:
			self.chat_state[chat_id] = [value]
		self.flush()

	def clear(self, chat_id: str) -> None:
		self.chat_state[chat_id] = []
		self.flush()

	def to_str(self, chat_id: str) -> str:
		masks = self.get_masks(chat_id)
		return "no masks" if masks == [] else "masks: " + str.join(", ", masks)

	def validate(self, chat_id: str, text: str) -> bool:
		masks = self.get_masks(chat_id)
		return any(map(lambda mask: mask in text, masks))

	def get_masks(self, chat_id: str):
		return self.chat_state[chat_id] if chat_id in self.chat_state else []

	def flush(self) -> None:
		with open(state_file, "w") as write_file:
			json.dump(self.chat_state, write_file)


masks = State()


@bot.message_handler(commands=["help"])
def help(message):
	bot.reply_to(
		message,
		"""
hi.
agrippina pins links so you can check them out later.


/pin to specify which links you would like to pin
usage: /pin spotify soundcloud

/show to view the masks you use

/clear to clear the masks list


note that agripipina needs administrator rights to pin messages in chats.
		""",
	)


@bot.message_handler(commands=["show"])
def show_masks(message: Message):
	bot.send_message(message.chat.id, masks.to_str(str(message.chat.id)))


@bot.message_handler(commands=["pin"])
def add_masks(message: Message):
	user_input = message.text if message.text else ""
	for mask in user_input.split()[1:]:
		masks.append(str(message.chat.id), mask)
	if message.text == "/pin":
		text = "usage: /pin spotify soundcloud"
		bot.send_message(message.chat.id, text)
	show_masks(message)


@bot.message_handler(commands=["clear"])
def clear_masks(message: Message):
	masks.clear(str(message.chat.id))
	show_masks(message)


def process_masks(message: Message) -> bool:
	entities = message.entities if message.entities else []
	user_input = message.text if message.text else ""
	for entity in entities:
		text = user_input[entity.offset : entity.length]
		has_masks = masks.validate(str(message.chat.id), text)
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
