FROM python:3.9-slim

# Instalar dependencias necesarias para Selenium, Firefox y GeckoDriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    firefox-esr \
    && wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-linux64.tar.gz \
    && tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin/ \
    && rm /tmp/geckodriver.tar.gz \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["tail", "-f", "/dev/null"]
