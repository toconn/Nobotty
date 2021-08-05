#!/usr/bin/env python3

from dataclasses import dataclass


@dataclass
class Command:
	command: str
	parameter: str = None


@dataclass
class User:
	id: int
	name: str
