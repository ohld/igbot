from ._version import __version__
del _version

from .api import API
from .bot import Bot
from . import utils

assert all((API, Bot, utils))  # silence pyflakes
