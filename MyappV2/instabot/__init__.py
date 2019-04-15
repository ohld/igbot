from .api import API
from .bot import Bot
from . import utils

assert all((API, Bot, utils))  # silence pyflakes
