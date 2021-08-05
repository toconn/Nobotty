#!/usr/bin/env python3

from os import listdir
from os.path import join
from fnmatch import filter
from sys import exit

from shared.utils import *
from bot_utils import *


HELP_TEXT = """<b>Help:</b>

/help - This Message
/start - Start the Bot
/status - Bot Status

/git-source - Source Code on Git
/speedsheets - Telegram SpeedSheets

/8-ball - Ask 🎱
/doh - Doh!
/jibber - Jibber Jabber
/klaxon - Sound the Alarm!
/llama - Llama Llama Llama l
/norris - Chuck Norris
/who-knows - Who knows?
"""

ALT_HELP_TEXT = """<b>Alt Help:</b>

/anvil - Anvil Rocks!
/brick - Brick!
/cake - Is there cake?
/first - Who goes first?

/list-simpsons - List available Simpson quotes.

"""

SPEEDSHEETS_TEXT = """Telegram Speedsheets:

<a href="https://speedsheet.io/s/telegram">Telegram SpeedSheet</>
<a href="https://speedsheet.io/s/aiogram">aiogram SpeedSheet</>
"""

CAKE_PHOTO_FILE = "cake.jpg"
DOH_PHOTO_FILE = "homer-doh.png"
KLAXON_AUDIO_FILE = "klaxon.wav"
LLAMA_PHOTO_FILE = "llama.png"

ANVIL_FILES = "anvil*.jpg"
BRICK_FILES = "brick*.jpg"
SIMPSON_FILES = "simpson*.wav"

CHUCK_NORRIS = [
		'Chuck Norris died 30 years ago. Death just hasn\'t had the courage to tell him yet.',
		'Chuck Norris has a grizzly bear carpet. The bear isn\'t dead. It is just too afraid to move.',
		'Chuck Norris doesn\'t flush the toilet, he scares the shit out of it.',
		'Death once had a near Chuck Norris experience.',
		'When Chuck Norris crosses the road, cars look both ways.',
		'Chuck Norris counted to infinity. Twice.',
		'A cobra once bit Chuck Norris\'s leg. After 5 days of excruciating pain, the cobra died.',
		'Chuck Norris can hear sign language.',
		'Chuck Norris can kill two stones with one bird.',
		'Chuck Norris doesn\'t dial wrong numbers, you pick up the wrong phone.',
		'Chuck Norris can unscramble an egg.',
		'Chuck Norris can hit so hard, your blood will bleed.',
		'When the Boogeyman goes to sleep, he checks his closet for Chuck Norris.',
		'Chuck Norris sleeps with a pillow beneath his gun.',
		'Chuck Norris doesn\'t cheat death. He wins fair and square.',
		'Chuck Norris\'s dog learned to clean up after itself. Chuck Norris doesn\'t take shit from anyone.',
		'Chuck Norris can cut a knife with butter.',
		'The only time Chuck Norris was wrong was when he though he made a mistake.',
		'Jesus can walk on water. Chuck Norris can swim on land.',
		'Chuck Norris doesn\'t use the force. The force uses Chuck Norris.',
		'There used to be a street called Chuck Norris but they changed the name because nobody crosses Chuck Norris and lives.'
]

EIGHT_BALL = [
		"It is Certain",
		"It is decidedly so",
		"Without a doubt",
		"Yes definitely",
		"You may rely on it",
		"As I see it, yes",
		"Most likely",
		"Outlook good",
		"Yes",
		"Signs point to yes",
		"Reply hazy, try again",
		"Ask again later",
		"Better not tell you now",
		"Cannot predict now",
		"Concentrate and ask again",
		"Don't count on it",
		"My reply is no",
		"My sources say no",
		"Outlook not so good",
		"Very doubtful",
]

MR_T = [
		'I believe in the Golden Rule - The Man with the Gold... Rules.',
		'Somedays you eat the bear, somedays the bear eats you.',
		'When I was growing up, my family was so poor we couldn\'t afford to pay attention.',
		'When I was old enough to change my name, I changed it to Mr. T so that the first word out of someone\'s mouth was \'Mister,\' a sign of respect.',
		'I don\'t like magic - but I have been known to make guys disappear.',
		'I\'m a Christian - I really don\'t believe in UFOs.',
		'It takes a smart guy to play dumb.',
		'Anger - use it, but don\'t lose it!',
		'I pitty the fool!',
		'First name Mr, middle name \'period\', last name T!',
		'Calvin Klein and Gloria Vanderbilt don\'t wear clothes with your name on it, so why should you wear their name?',
		'People ask me what the "T" stands for in my name. If you\'re a man, the "T" stands for tough. If you\'re a woman or child, it stands for tender!'
]

PLAYERS = [
		'Bill',
		'Marco',
		'Tim',
 	]


def read_files (data_dir, file_filter):
	return filter (listdir (data_dir), file_filter)


## Bot Commands ###########################################

class BotCommands:

	def __init__(self, bot, dispatcher, settings):

		self.bot = bot
		self.dispatcher = dispatcher

		self.bot_name = settings.bot_name
		self.data_dir = settings.data_dir

		self.anvil = read_files(self.data_dir, ANVIL_FILES)
		self.brick = read_files(self.data_dir, BRICK_FILES)
		self.simpsons = read_files(self.data_dir, SIMPSON_FILES)

		self._configure_commands (dispatcher)


	def _configure_commands(self, dispatcher):

		dispatcher.register_message_handler (self.command_show_help, commands = {'help'})
		dispatcher.register_message_handler (self.command_show_alt_help, commands = {'alt_help', 'alt-help', 'alt', 'alt.help'})
		dispatcher.register_message_handler (self.command_start, commands = {'start'})
		dispatcher.register_message_handler (self.command_status, commands = {'status', 'stat', 'stats'})
		dispatcher.register_message_handler (self.command_anvil, commands = {'anvil'})
		dispatcher.register_message_handler (self.command_brick, commands = {'brick', 'brick!'})
		dispatcher.register_message_handler (self.command_cake, commands = {'cake', 'the', 'thecakeisalie', 'the_cake_is_a_lie', 'lie'})
		dispatcher.register_message_handler (self.command_chuck_norris, commands = {'chuck', 'norris', 'chucknorris', 'chuck_norris'})
		dispatcher.register_message_handler (self.command_doh, commands = {'doh', 'doh!'})
		dispatcher.register_message_handler (self.command_ask_eight_ball, commands = {'8-ball', '8_ball', '8', '8ball', 'ball', '🎱'})
		dispatcher.register_message_handler (self.command_jibber_jabber, commands = {'jibber', 'jabber', 'jibberjabber', 'jibber_jabber'})
		dispatcher.register_message_handler (self.command_klaxon, commands = {'klaxon'})
		dispatcher.register_message_handler (self.command_list_simpsons, commands = {'list-simpsons', 'list_simpsons', 'simpsons'})
		dispatcher.register_message_handler (self.command_llama, commands = {'llama'})
		dispatcher.register_message_handler (self.command_show_source_repo, commands = {'git-source', 'git_source', 'git', 'github', 'gitsource', 'source', 'sourcecode', 'source_code'})
		dispatcher.register_message_handler (self.command_show_speedsheets, commands = {'speedsheets', 'speed', 'sheet', 'sheets'})
		dispatcher.register_message_handler (self.command_who_is_first, commands = {'who-is-first', 'who_is_first', 'who-goes-first', 'who_goes_first', 'first', 'pick'})
		dispatcher.register_message_handler (self.command_who_knows, commands = {'who', 'who_knows'})
		# dispatcher.register_message_handler (self.command_stop, commands = {'stop', 'exit'})


	async def command_cake(self, message):

		log_command ("cake", message)

		await self._reply_photo (message, CAKE_PHOTO_FILE)


	async def command_anvil(self, message):

		log_command ("anvil", message)

		await self._reply_photo (message, pick_one_and_print (self.anvil))


	async def command_brick(self, message):

		log_command ("brick", message)

		await self._reply_photo (message, pick_one_and_print (self.brick))


	async def command_chuck_norris(self, message):

		log_command ("chuck norris", message)

		await reply (message, pick_one_and_print (CHUCK_NORRIS))


	async def command_doh(self, message):

		log_command ("doh", message)

		await self._reply_photo (message, DOH_PHOTO_FILE)
		await self._reply_audio (message, pick_one_and_print(self.simpsons))


	async def command_ask_eight_ball(self, message):

		log_command ("ask 8 ball", message)

		await reply (message, "🎱  " + pick_one_and_print (EIGHT_BALL))


	async def command_jibber_jabber(self, message):

		log_command ("jibber jabber", message)

		command = parse_command (message)

		if command.parameter:
			await reply (message, f"Got your jibber jabber right here:\n\n{command.parameter}!")
		else:
			await reply (message, pick_one_and_print (MR_T))
			await reply (message, "<i>- Mr. T</i>")


	async def command_klaxon(self, message):

		log_command ("Command - klaxon", message)
		await self._reply_audio (message, KLAXON_AUDIO_FILE)


	async def command_list_simpsons(self, message):

		log_command ("list simpsons", message)

		await reply (message, "Met The Simpson:\n\n" + "\n".join (self.simpsons))


	async def command_llama(self, message):

		log_command ("llama", message)

		await self._reply_photo (message, LLAMA_PHOTO_FILE)


	async def command_show_alt_help(self, message):

		log_command ("show alt help", message)

		await reply (message, ALT_HELP_TEXT)


	async def command_show_help(self, message):

		log_command ("show help", message)

		await reply (message, HELP_TEXT)


	async def command_show_source_repo(self, message):

		log_command ("show source repo", message)

		await reply (message, 'Source on Github:\n<a href="https://github.com/toconn/nobotty">https://github.com/toconn/nobotty</a>')


	async def command_show_speedsheets(self, message):

		log_command ("show speedsheets", message)

		await reply (message, SPEEDSHEETS_TEXT)


	async def command_start(self, message):

		log_command ("start", message)

		await reply (message, f"'ello {message.from_user.first_name}!")
		await reply (message, HELP_TEXT)


	async def command_status(self, message):

		log_command ("start", message)

		await reply (message, f"{self.bot_name}:\nI am completely operational, and all my circuits are functioning perfectly.")


	async def command_stop(self, message):

		print ("Stopping.")

		await reply (message, "stopping.")
		# self.dispatcher.stop_polling()
		os.exit()


	async def command_who_is_first(self, message):

		log_command ("who is first", message)

		await reply (message, pick_one_and_print (PLAYERS))


	async def command_who_knows(self, message):

		log_command ("Command - who knows", message)

		if should_i_weighted(30):
			await reply (message, "Nobotty knows!")
		else:
			await reply (message, "Nobody knows!")
			if should_i():
				await reply (message, "Maybe aliens?")


	def _path(self, file_name):
		return join (self.data_dir, file_name)

	
	async def _reply_audio (self, message, file_name):
		await reply_audio (message, self._path(file_name))

	
	async def _reply_photo (self, message, file_name):
		await reply_photo (message, self._path(file_name))



