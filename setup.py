from setuptools import setup


def get_version_and_cmdclass(package_name):
    import os
    from importlib.util import module_from_spec, spec_from_file_location
    spec = spec_from_file_location('version',
                                   os.path.join(package_name, '_version.py'))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__version__, module.cmdclass


version, cmdclass = get_version_and_cmdclass('instabot')

setup(
    name='instabot',
    packages=['instabot', 'instabot.bot', 'instabot.api'],
    version=version,
    cmdclass=cmdclass,
    description='Cool Instagram bot scripts and API python wrapper.',
    author='Daniil Okhlopkov, Evgeny Kemerov',
    author_email='ohld@icloud.com, eskemerov@gmail.com',
    url='https://github.com/instagrambot/instabot',
    download_url='https://github.com/instagrambot/instabot/tarball/0.4.2',
    keywords=['instagram', 'bot', 'api', 'wrapper'],
    classifiers=[],
    install_requires=['tqdm', 'requests-toolbelt', 'requests', 'schedule', 'future', 'six', 'huepy'],
)
