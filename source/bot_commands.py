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

/git_source - Source Code on Git

/doh - Doh!
/jibber - Some Jibber Jabber!
/klaxon - Klaxon!
/llama - Llama!
/norris - Chuck Norris
/speedsheets - Telegram SpeedSheets
/who_knows - Who knows?
"""

SPEEDSHEETS_TEXT = """Telegram Speedsheets:

<a href="https://speedsheet.io/s/telegram">Telegram SpeedSheet</>
<a href="https://speedsheet.io/s/aiogram">aiogram SpeedSheet</>
"""

CAKE_PHOTO_FILE = "cake.jpg"
DOH_PHOTO_FILE = "homer-doh.png"
KLAXON_AUDIO_FILE = "klaxon.wav"
LLAMA_PHOTO_FILE = "llama.png"

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


def read_simpsons_files(data_directory):
	return filter (listdir (data_directory), "simpson*.wav")


## Bot Commands ###########################################

class BotCommands:

	def __init__(self, bot, dispatcher, settings):

		self.bot = bot
		self.dispatcher = dispatcher

		self.bot_name = settings.bot_name
		self.data_dir = settings.data_dir

		self.simpsons = read_simpsons_files (self.data_dir)

		self._configure_commands (dispatcher)


	def _configure_commands(self, dispatcher):

		dispatcher.register_message_handler (self.command_show_help, commands = {'help'})
		dispatcher.register_message_handler (self.command_start, commands = {'start'})
		dispatcher.register_message_handler (self.command_status, commands = {'status', 'stat', 'stats'})
		dispatcher.register_message_handler (self.command_cake, commands = {'cake', 'the', 'thecakeisalie', 'the_cake_is_a_lie', 'lie'})
		dispatcher.register_message_handler (self.command_chuck_norris, commands = {'chuck', 'norris', 'chucknorris', 'chuck_norris'})
		dispatcher.register_message_handler (self.command_doh, commands = {'doh', 'doh!'})
		dispatcher.register_message_handler (self.command_jibber_jabber, commands = {'jibber', 'jabber', 'jibberjabber', 'jibber_jabber'})
		dispatcher.register_message_handler (self.command_klaxon, commands = {'klaxon'})
		dispatcher.register_message_handler (self.command_list_simpsons, commands = {'list_simpsons', 'simpsons'})
		dispatcher.register_message_handler (self.command_llama, commands = {'llama'})
		dispatcher.register_message_handler (self.command_show_source_repo, commands = {'git_source', 'git', 'github', 'gitsource', 'source', 'sourcecode', 'source_code'})
		dispatcher.register_message_handler (self.command_show_speedsheets, commands = {'speedsheets', 'speed', 'sheet', 'sheets'})
		dispatcher.register_message_handler (self.command_who_knows, commands = {'who', 'who_knows'})
		# dispatcher.register_message_handler (self.command_stop, commands = {'stop', 'exit'})


	async def command_cake(self, message):

		log_command ("cake", message)

		await reply_photo (message, self._path(CAKE_PHOTO_FILE))


	async def command_chuck_norris(self, message):

		log_command ("chuck norris", message)

		await reply (message, pick_one_and_print (CHUCK_NORRIS))


	async def command_doh(self, message):

		log_command ("doh", message)

		await reply_photo (message, self._path(DOH_PHOTO_FILE))
		await reply_audio (message, self._path (pick_one_and_print(self.simpsons)))


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
		await reply_audio (message, self._path(KLAXON_AUDIO_FILE))


	async def command_list_simpsons(self, message):

		log_command ("list simpsons", message)

		await reply (message, "Met The Simpson:\n\n" + "\n".join (self.simpsons))


	async def command_llama(self, message):

		log_command ("llama", message)

		await reply_photo (message, self._path(LLAMA_PHOTO_FILE))


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


	async def command_who_knows(self, message):

		log_command ("Command - who knows", message)

		await reply (message, "Nobody knows!")
		if should_i():
			await reply (message, "Maybe aliens?")


	def _path(self, file_name):

		return join (self.data_dir, file_name)


