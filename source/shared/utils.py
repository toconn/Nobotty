#!/usr/bin/env python3

from random import choice
from random import randrange
from random import sample
from shared.console import *


def pick_one(items):
	return sample(items, 1)[0]


def pick_one_and_print(items):

	item = pick_one(items)

	print_indent (1, "Picked", item)
	nl()

	return item


def should_i():
	return choice([True, False])


def should_i_weighted(percent = 50):
	return randrange(101) <= percent
