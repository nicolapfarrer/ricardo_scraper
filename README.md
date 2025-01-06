# Ricardo.ch Telegram Bot 🤖

Automated scraper for Ricardo.ch that sends notifications via Telegram for new listings based on custom search criteria.

## Features ✨

- 🔄 Automated daily search
- 🔐 Proxy support
- 📱 Telegram notifications
- 🐳 Docker support

## Prerequisites 📋

- Python 3.11.8 (other versions may work but are untested)
- Docker & Docker Compose
- Telegram Bot Token
- Telegram Chat ID
- Ricardo.ch Search Criteria

## Quick Start 🚀

### Deployment with Docker 🐳

1. Create environment file (.env)
   - `BOT_TOKEN`: Telegram Bot API token
   - `CHAT_ID`: Telegram chat ID for notifications
   - `PROXY_LIST_URL`: URL for proxy list
   - `SCHEDULE_TIME`: Daily execution time (HH:MM)

2. Configure search criteria (search.yaml)

Example usage:
```yaml
graphics_cards:
  categorySeoSlug: grafikkarte-39204
  sort: newest
laptops:
  categorySeoSlug: notebooks-39272
  sort: best
```

3. Build and run with Docker Compose:
```bash
docker-compose build
```
```bash
docker-compose up -d
```

Example 

docker-compose.yml

:
```yaml
services:
  app:
    image: ghcr.io/nicolapfarrer/ricardo_scraper:latest
    volumes:
      - /home/user/ricardo_scraper:/app # location where the config will live
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - CHAT_ID=${CHAT_ID}
      - PROXY_LIST_URL=${PROXY_LIST_URL}
      - SCHEDULE_TIME=${SCHEDULE_TIME}
      - TZ=Europe/Zurich # Default is UTC
    networks:
      - scraper_network

networks:
  scraper_network:
    driver: bridge
```

### Local Deployment 🖥️

1. Clone the repository
```bash
git clone https://github.com/nicolapfarrer/ricardo_scraper
cd ricardo_scraper
```

2. Create environment file (.env)
   - `BOT_TOKEN`: Telegram Bot API token
   - `CHAT_ID`: Telegram chat ID for notifications
   - `PROXY_LIST_URL`: URL for proxy list
   - `SCHEDULE_TIME`: Daily execution time (HH:MM)

3. Configure search criteria (search.yaml)

Example usage:
```yaml
graphics_cards:
  categorySeoSlug: grafikkarte-39204
  sort: newest
laptops:
  categorySeoSlug: notebooks-39272
  sort: best
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

5. Run the scraper
```bash
python scraper.py
```

## Project Structure 📁

```
ricardo-telegram-bot/
├── bot.py           # Telegram bot functionality
├── main.py          # Core scraping logic
├── scheduler.py     # Scheduled task execution
├── Dockerfile       # Container configuration
├── docker-compose.yml
├── requirements.txt
├── .env
└── search.yaml
```

## Contributing 🤝

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## License 📄

GPL License 