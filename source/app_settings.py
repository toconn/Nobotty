#!/usr/bin/env python3

from dataclasses import dataclass
from shared.settings_locator import *
from shared.settings import *
from data import *


SETTINGS_LOCATION = Location(
	settings_file_name = "nobotty.settings",
	environment_name = "NOBOTTY_HOME")

DATA_DIR_SETTING = "data.dir"
LOG_FILE_SETTING = "log.file"
LOG_TO_CONSOLE_SETTING = "log.to.console"
BOT_NAME_SETTING = "bot.name"
BOT_TOKEN_SETTING = "bot.token"
OWNER_ID_SETTING = "owner.id"
OWNER_NAME_SETTING = "owner.name"

REQUIRED_SETTINGS = [
		DATA_DIR_SETTING,
		LOG_FILE_SETTING,
		BOT_NAME_SETTING,
		BOT_TOKEN_SETTING,
		OWNER_ID_SETTING,]


## Settinsg ################################################

@dataclass
class AppSettings:
	data_dir: str
	log_file: str
	log_to_console: bool
	bot_name: str
	bot_token: str
	owner: str


def read_app_settings():

	location = locate (SETTINGS_LOCATION)
	settings = Settings (location)
	settings.validate (REQUIRED_SETTINGS)

	return to_app_settings (settings)


def to_app_settings(settings):

	return AppSettings(
		data_dir = settings.get(DATA_DIR_SETTING),
		log_file = settings.get(LOG_FILE_SETTING),
		log_to_console = settings.get_boolean(LOG_TO_CONSOLE_SETTING, True),
		bot_name = settings.get(BOT_NAME_SETTING),
		bot_token = settings.get(BOT_TOKEN_SETTING),
		owner = User (
			id = settings.get(OWNER_ID_SETTING),
			name = settings.get(OWNER_NAME_SETTING)),
		)

