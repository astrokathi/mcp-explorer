FROM python:3.11-slim
WORKDIR /app

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Install Node.js for MCP Servers (npx)
RUN apt-get update && apt-get install -y nodejs npm chromium && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install .

COPY . .

EXPOSE 8000

CMD ["chainlit", "run", "ui/app.py", "--host", "0.0.0.0", "--port", "8000"]
