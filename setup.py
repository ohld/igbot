from setuptools import setup
setup(
    name='instabot',
    packages=['instabot', 'instabot.bot', 'instabot.api'],
    version='0.3.3.20',
    description='Cool Instagram bot scripts and API python wrapper.',
    author='Daniil Okhlopkov',
    author_email='ohld@icloud.com',
    url='https://github.com/instagrambot/instabot',
    download_url='https://github.com/instagrambot/instabot/tarball/0.3.3.20',
    keywords=['instagram', 'bot', 'api', 'wrapper'],
    classifiers=[],
    install_requires=['tqdm', 'requests-toolbelt', 'requests', 'schedule'],
)
