# Contributing to Instabot

👍🎉 First off, thanks for taking the time to contribute! 🎉👍

## How can I help the project?

You can:
* Put the star into the [Instabot main repository](https://github.com/instagrambot). To do this, click on the star here https://github.com/instagrambot at top right corner. Mind that GitHub registration is required (for free).
* Login to [Telegram Group](https://t.me/instabotproject) and help newcomers to understand the installation and configuration of Instabot.
* Tell everywhere about our project! It will be enough to throw off the link: https://instagrambot.github.io.
* Find bugs and describe them in [Issues](https://github.com/instagrambot/instabot/issues) section, be sure to attach the _screenshots_ and _commands_ that you entered. This will help correct these errors and make Instabot better!
* If you are a developer, correct these bugs and errors! Do this via Pull Request, don't forget the PEP8 standard.
* If you have a brilliant Instabot usage example or even the independent project connected with instagram, [tell us](https://t.me/instabotproject) about it!

## Adding the new docs
If you want to add a new documentation page in any language please follow the guide below.

1. If your docs have not been written in english, please translate your doc in English too and add it into [en/](https://github.com/instagrambot/docs/blob/master/en/) folder.
2. Make sure that your doc is written descriptive enough. If you use pictures, please upload them into [img/](https://github.com/instagrambot/docs/blob/master/img/) folder.
3. Add the link to your doc into the existing docs to make other users find your page.
4. Create pull request with your docs.

## Translate the Docs into your language

1. Fork the [repository](https://github.com/instagrambot/instabot).
2. Create a folder with the name of your country in the abbreviation.
3. Copy all the files from the `/en/` folder to your earlier created folder.
4. Translate the files into your language, leaving the file structure of the previous one (paragraphs etc).
5. Add the link to your docs in the main [README.md](https://github.com/instagrambot/docs/blob/master/README.md) file. Don't forget to add the flag emoji!
6. Create pull request.

***Thank you for supporting the project!***

## For Developers

Install the dependencies using [pipenv](https://github.com/pypa/pipenv): `pipenv install`

See `.travis.yml` for the most up to date test and lint commands.

We use [`pre-commit`](https://pre-commit.com) to keep a consistent code style, so ``pip install pre_commit`` and run
```bash
pre-commit install  # only need to do this once!
```
to install the hooks.
These will then automatically run upon each commit.
