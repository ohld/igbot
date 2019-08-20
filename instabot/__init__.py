from . import utils
from .api import API
from .bot import Bot

assert all((API, Bot, utils))  # silence pyflakes
