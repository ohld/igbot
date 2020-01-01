FROM python:3.7.2-slim

WORKDIR /app

COPY Pipfile .
RUN pip install pipenv
RUN pipenv install
COPY . .

VOLUME /app/examples/autopost/pics/

CMD [ "pipenv", "run", "python", "examples/multi_script_CLI.py"]
