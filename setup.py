from distutils.core import setup
setup(
  name = 'instabot',
  packages = ['instabot', 'instabot.bot', 'instabot.api'],
  version = '0.2.5.8',
  description = 'Cool Instagram bot scripts and API python wrapper.',
  author = 'Daniil Okhlopkov',
  author_email = 'ohld@icloud.com',
  url = 'https://github.com/ohld/instabot',
  download_url = 'https://github.com/ohld/instabot/tarball/0.2.5.8',
  keywords = ['instagram', 'bot', 'api'],
  classifiers = [],
  install_requires=['tqdm', 'requests-toolbelt', 'requests'],
)
