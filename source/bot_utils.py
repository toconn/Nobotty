#!/usr/bin/env python3

from aiogram.utils.exceptions import *
from aiogram.utils import executor
from dataclasses import dataclass
from app_log import *
from data import *


## Bot Utils ###############################################

def report_error(command):

	async def wrapper(*args, **kwargs):

			try:
				
				return await command(*args, **kwargs)

			except RetryAfter as e:

				log (f"Error - ID {user.id}: Flood Limit Exceeded. Sleep {e.timeout} Seconds.")
				await asyncio.sleep(e.timeout)

				return await command(*args, **kwargs)

			except BotBlocked:

				log (f"Error - ID {user.id}: Blocked by User")
			
			except ChatNotFound:

				log (f"Error - ID {user.id}: Invalid User ID")
			
			except UserDeactivated:

				log (f"Error - ID {user.id}: User is Deactivated.")
			
			except TelegramAPIError:

				log (f"Error - ID {user.id}: API Failed")

	return wrapper


def log_command(command, message):

	log (command + ":")
	nl()
	log_indent (1, "From", f"{message.from_user.first_name} / {message.chat.id}")
	log_indent (1, "Message", message.text)
	nl()


@report_error
async def reply (message, response):
	await message.answer (response)


@report_error
async def reply_audio (message, audio_file):

	with open (audio_file, 'rb') as file:
		audio = file.read()
		await message.answer_audio(audio)


@report_error
async def reply_photo (message, photo_file):
	with open (photo_file, 'rb') as file:
		await message.answer_photo(file)


@report_error
async def send_message (bot, user, message):

	log (f"sending message to {user.name} [{user.id}]...")
	
	await bot.send_message (user.id, message)

	log ("sent.")
	nl()


## Command Utils ###########################################

def normalize_command (command):
	return command.removeprefix("/").strip().lower()


def normalize_parameter (parameter):
	return parameter.strip()


def parse_command(message):

	if " " not in message.text:
		return Command (normalize_command (message.text))

	command, parameter = message.text.split(" ", 1)

	return Command(
			normalize_command (command),
			normalize_parameter (parameter))
