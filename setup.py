from setuptools import setup

with open('requirements.txt') as f:
    requirements = [x.strip() for x in f.readlines()]

setup(
    name='instabot',
    packages=['instabot', 'instabot.bot', 'instabot.api'],
    version='0.4',
    description='Cool Instagram bot scripts and API python wrapper.',
    author='Daniil Okhlopkov, Evgeny Kemerov',
    author_email='ohld@icloud.com, eskemerov@gmail.com',
    url='https://github.com/instagrambot/instabot',
    download_url='https://github.com/instagrambot/instabot/tarball/0.4',
    keywords=['instagram', 'bot', 'api', 'wrapper'],
    classifiers=[],
    install_requires=requirements,
)
