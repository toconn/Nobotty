#!/usr/bin/env python3

from collections import Mapping
from collections import MutableMapping
from datetime import datetime
from shared.random import Random
from shared.console import *


random = Random()


def format_timedelta(timedelta_1):

    seconds = timedelta_1.seconds
    hours = int (seconds // 3600)
    seconds = seconds % 3600
    minutes = int (seconds // 60)
    seconds = int (seconds % 60)

    if timedelta_1.days > 0:
        return f"{timedelta_1.days} days {hours}:{minutes:02}:{seconds:02}"

    return f"{hours}:{minutes:02}:{seconds:02}"


def format_timedelta_from_now(datetime_1):
    return format_timedelta (datetime.today() - datetime_1)


def not_empty(value):
    return value != None and value != ""


def pick_one(items):
	# return sample(items, 1)[0]
	return random.pick_one(items)


def pick_one_and_print(items):

	item = pick_one(items)

	print_indent (1, "Picked", item)
	nl()

	return item


def should_i():
	return random.boolean()


def should_i_weighted(percent = 50):
	return random.boolean_weighted (percent / 100)
