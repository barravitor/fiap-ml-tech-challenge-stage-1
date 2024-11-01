FROM python:3.10.12

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libxss1 \
    libappindicator3-1 \
    libgconf-2-4 \
    libnss3 \
    fonts-liberation \
    libgbm-dev \
    xvfb \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir webdriver-manager

WORKDIR /app

COPY ../requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./cron_jobs/app /app/app

COPY ../shared /app/shared

CMD ["python3", "-m", "app.scraping"]