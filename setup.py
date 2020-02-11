from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="instabot",
    version="0.107.0",
    description="Instagram bot scripts for promotion and API python wrapper.",
    long_description=long_description,
    author="Daniil Okhlopkov, Evgeny Kemerov",
    author_email="danokhlopkov@gmail.com, eskemerov@gmail.com",
    license="Apache Software License 2.0",
    url="https://github.com/instagrambot/instabot",
    keywords=["instagram", "bot", "api", "wrapper"],
    install_requires=[
        "certifi>=2019.11.28",
        "chardet>=3.0.4",
        "future>=0.18.2",
        "huepy>=1.2.1",
        "idna>=2.8",
        "pysocks>=1.7.1",
        "pytz>=2019.3",
        "requests>=2.22.0",
        "requests-toolbelt>=0.9.1",
        "responses>=0.10.9",
        "schedule>=0.6.0",
        "six>=1.14.0",
        "tqdm>=4.41.1",
        "urllib3>=1.25.7",
        "mock>=3.0.5",
        "moviepy>=1.0.1",
        "Pillow>=6.2.2",
        "pytest>=4.6.9",
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
