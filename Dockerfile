FROM python:3.7.2-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "example/multi_script_CLI.py" ]
