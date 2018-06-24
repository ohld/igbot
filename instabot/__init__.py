from ._version import __version__
from .api import API
from .bot import Bot
from . import utils

assert all((API, Bot, utils, __version__))  # silence pyflakes
