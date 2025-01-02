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
Exaple usage:
```yaml
graphics_cards:
  categorySeoSlug: grafikkarte-39204
  sort: newest
laptops:
  categorySeoSlug: notebooks-39272
  sort: best
```

## Docker Deployment 🐳

Build and run with Docker Compose:
```bash
docker-compose up --build -d
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

GPL License - see 

LICENSE

 file for details
```