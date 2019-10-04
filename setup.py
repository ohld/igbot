from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="instabot",
    version="0.62.0",
    description="Instagram bot scripts for promotion and API python wrapper.",
    long_description=long_description,
    author="Daniil Okhlopkov, Evgeny Kemerov",
    author_email="danokhlopkov@gmail.com, eskemerov@gmail.com",
    license="Apache Software License 2.0",
    url="https://github.com/instagrambot/instabot",
    keywords=["instagram", "bot", "api", "wrapper"],
    install_requires=[
        "tqdm>=4.30.0",
        "requests>=2.21.0",
        "requests-toolbelt>=0.8.0",
        "schedule>=0.6.0",
        "pysocks>=1.6.8",
        "responses>=0.10.5",
        "future>=0.17.1",
        "six>=1.12.0",
        "huepy>=0.9.8.1",
        "pytz>=2019.1",
    ],
    classifiers=[
        # How mature is this project? Common values are
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Information Technology",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: Apache Software License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
)
