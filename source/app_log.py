#!/usr/bin/env python3

import logging
from os.path import join
from app_settings import *


LOG_FORMAT = "%(asctime)s    %(threadName)s    %(message)s"
LOG_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LOGGER = None
LOG_TO_CONSOLE = True

COLUMN_1_WIDTH = 30
COLUMN_SEPARATOR = ': '
HEADING_WIDTH = 60
INDENT = '    '


## Log Core ################################################


def log(text = ""):

	LOGGER.info (text)

	if LOG_TO_CONSOLE:
		print (text)


def log_error (text):

	LOGGER.error (text)
	
	if LOG_TO_CONSOLE:
		print ("Error", text)


def new_log_handler(path):

	handler = logging.FileHandler(path)
	handler.setLevel (logging.DEBUG)
	handler.setFormatter (logging.Formatter (
		fmt = LOG_FORMAT,
		datefmt = LOG_DATETIME_FORMAT))

	return handler


def new_logger(path):

	logger = logging.getLogger ("thumbnails")
	logger.addHandler (new_log_handler (path))
	logger.setLevel (logging.DEBUG)

	return logger


def start_logger():

	settings = read_app_settings()
	LOG_TO_CONSOLE = settings.log_to_console

	return new_logger (settings.log_file)


LOGGER = start_logger()


## Log Helpers #############################################

def dot_dot_dot(text, length):

	if text and len(text) > length:
		return text[:length + 1] + "..."

	return text


def heading(heading):
	log_heading(heading)


def nl():
	"""Logs a new line."""
	log("")


def log_(value, value_2 = None):

	if value == None:
		log_("[None]", value_2)
		return

	if value_2 == None:
		log(value)
		return

	try:
		log(value.ljust(COLUMN_1_WIDTH) + COLUMN_SEPARATOR + value_2)
	except TypeError:
		try:
			log(value.ljust(COLUMN_1_WIDTH) + COLUMN_SEPARATOR + str(value_2))
		except TypeError:
			log(value.ljust(COLUMN_1_WIDTH) + COLUMN_SEPARATOR + "[Non Logable Type]")


def log_2(value, value_2 = None):
	log_(value, value_2)


def log_double(value, value_2 = None):
	log_(value, value_2)
	nl()


def log_error(value, value_2 = None, show_trace = False):

	if value_2:
		log_ ("Error", value)
		error = value_2
	else:
		log_ ("Error")
		error = value1

	nl()
	log_indent (1, "Type", type(error)) 

	if error.args and error.args[0]:
		log_indent (1, "Message", error.args[0])
	nl()

	if show_trace:
		log(traceback.format_exc())
		nl()


def log_head(heading):
	log_heading(heading)


def log_heading(heading):

	nl()
	log(("** " + heading + "  ").ljust(HEADING_WIDTH, "*"))
	nl()


def log_indent(value, value_2, value_3 = None):

	indent = INDENT * value

	if type (value_3) is str and "\n" in value_3:
		value_3 = "\n\n" + indent + ("\n" + indent).join (value_3.splitlines())

	log_(indent + value_2, value_3)


def log_is_empty(value):

	log_("value", str(value))
	nl()

	# Test Is List

	if type(value) is list:
		log("  is list:    List")
	else:
		log("  is list:    Not List")

	if type(value) == list:
		log("  = list:     List")
	else:
		log("  = list:     Not List")

	nl()

	if value:
		log("  value:      Not Empty")
	else:
		log("  value:      Empty")

	if not value:
		log("  not value:  Empty")
	else:
		log("  not value:  Not Empty")

	nl()

	if value is None:
		log("  is None:    None")
	else:
		log("  is None:    Not None")

	if isinstance(value, list):
		if len(value):
			log("  len:        Not Empty")
		else:
			log("  len:        Empty")

	nl()


def log_lines(value, value_2 = None):
	if value_2:
		log(value + COLUMN_SEPARATOR)
		nl()
		for item in value_2:
			log_indent(1, item)
	else:
		for item in value:
			log(item)
	nl()


def log_list(value, value_2 = None):
	log_lines(value, value_2)


def log_middle(value, value_2 = None):
	nl()
	log_(value, value_2)
	nl()


def log_short_heading(heading):
	nl()
	log(("** " + heading + " **"))
	nl()


def log_title(title):

	nl()
	log("*" * HEADING_WIDTH)
	log(("** " + title + " ").ljust(HEADING_WIDTH - 2) + "**")
	log("*" * HEADING_WIDTH)
	nl()


def log_type(value, value_2 = None):
	if value_2:
		log_(value, type(value_2))
		log_(" ", value_2)
	else:
		log(type(value))
		log(value)


def log_value(value, value_2 = None):
	if value_2:
		log_(value, repr(value_2))
	else:
		log(repr(value))
