#!/usr/bin/env python3

from asyncio import run
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.types import ParseMode

from app_settings import *
from app_log import *
from bot_utils import *
from bot_commands import BotCommands


## Notification ############################################

async def notify_started(bot, settings):

	await send_message (bot, settings.owner, "Bot is up.")
	log ("Bot started.")


async def notify_stopped(bot, settings):

	await send_message (bot, settings.owner, "Bot stopped.")
	log ("Bot stopped.")


## Mair ####################################################

async def main():

	settings = read_app_settings()

	bot = Bot (token = settings.bot_token, parse_mode = ParseMode.HTML)

	dispatcher = Dispatcher (bot)
	commands = BotCommands (bot, dispatcher, settings)

	try:
		await notify_started(bot, settings)
		await dispatcher.start_polling()
	finally:
		await notify_stopped(bot, settings)
		await bot.close()


run (main())

