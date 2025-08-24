# Telegram Stock Analyst Bot 📈

A professional Telegram bot that provides real-time stock analysis with beautiful financial charts, powered by Perplexity AI and Yahoo Finance data.

![Bot Demo](https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## ✨ Features

- 📊 **Professional Financial Charts** - Dark theme charts similar to Yahoo Finance/Bloomberg
- 🤖 **AI-Powered Analysis** - Real-time market insights using Perplexity AI
- 📈 **Real-Time Data** - Live stock data from Yahoo Finance via yfinance
- 💼 **Comprehensive Metrics** - Market Cap, P/E Ratio, 52W Range, Volume, EPS
- 🎨 **Beautiful UI** - Professional dark theme matching financial platforms
- ⚡ **Fast Response** - Optimized for quick analysis and chart generation
- 🔍 **Smart Ticker Detection** - Automatically detects stock symbols in messages
- 📱 **Telegram Integration** - Seamless chart and data delivery via Telegram

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Perplexity AI API Key (from [perplexity.ai](https://www.perplexity.ai/settings/api))
- Optional: Chart-img API Key for additional charts

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/telegram-stock-analyst-bot.git
   cd telegram-stock-analyst-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   
   Edit the credentials in `main.py`:
   ```python
   TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
   PERPLEXITY_API_KEY = "your_perplexity_api_key"
   CHART_IMG_API_KEY = "your_chart_img_api_key"  # Optional
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

## 📋 Usage

### Basic Commands

- **Stock Analysis**: Send any ticker symbol
  ```
  AAPL
  Tesla stock
  What about $MSFT?
  ```

- **Detailed Analysis**: Use specific commands
  ```
  analyze AAPL
  chart TSLA
  info GOOGL
  ```

### Bot Response Flow

1. **Professional Chart** - Generated automatically for each request
2. **Financial Summary** - Key metrics displayed in organized format
3. **AI Analysis** - Powered by Perplexity AI with current market data
4. **Educational Insights** - Risk assessment and learning points

## 🛠️ Configuration

### Environment Variables (Recommended)

Create a `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
PERPLEXITY_API_KEY=your_perplexity_api_key
CHART_IMG_API_KEY=your_chart_img_api_key
```

### API Keys Setup

1. **Telegram Bot Token**:
   - Message [@BotFather](https://t.me/botfather)
   - Create a new bot with `/newbot`
   - Get your token

2. **Perplexity AI API Key**:
   - Visit [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
   - Generate API key
   - Add credits to your account

3. **Chart-img API Key** (Optional):
   - Visit [chart-img.com](https://chart-img.com)
   - Sign up and get API key for enhanced charts

## 📊 Chart Features

- **Dark Theme**: Professional financial platform styling
- **Real-Time Data**: Live price updates with 5-minute intervals for intraday
- **Multiple Timeframes**: 1D (5min), 5D (15min), 1M (daily)
- **Financial Metrics**: Market Cap, P/E, Volume, 52W Range displayed on chart
- **Price Indicators**: Current price with change percentage and color coding
- **Time Period Buttons**: Visual representation of available timeframes

## 🔧 Technical Details

### Architecture

```
telegram-stock-analyst-bot/
├── main.py                 # Main bot application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE               # MIT License
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
└── docs/                # Documentation
    ├── api.md           # API documentation
    ├── deployment.md    # Deployment guide
    └── troubleshooting.md # Common issues
```

### Dependencies

- `python-telegram-bot` - Telegram Bot API wrapper
- `yfinance` - Yahoo Finance data retrieval
- `pandas` - Data manipulation and analysis
- `matplotlib` - Chart generation
- `requests` - HTTP requests for APIs
- `plotly` - Advanced charting (optional)

### Error Handling

- **API Timeouts**: Graceful fallback when external APIs are slow
- **Data Validation**: Robust handling of missing or invalid stock data
- **Format Errors**: Pre-validation of all numeric formatting
- **Network Issues**: Automatic retry mechanisms with exponential backoff

## 🚀 Deployment

### Local Development

```bash
# Clone and setup
git clone https://github.com/yourusername/telegram-stock-analyst-bot.git
cd telegram-stock-analyst-bot
pip install -r requirements.txt

# Configure API keys in main.py or .env file
# Run the bot
python main.py
```

### Production Deployment

#### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

#### Using Heroku

```bash
# Install Heroku CLI and login
heroku create your-bot-name
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set PERPLEXITY_API_KEY=your_key
git push heroku main
```

#### Using VPS/Cloud

```bash
# Setup systemd service
sudo nano /etc/systemd/system/stock-bot.service

# Enable and start
sudo systemctl enable stock-bot
sudo systemctl start stock-bot
```

## 📈 Performance

- **Response Time**: < 3 seconds for chart generation
- **API Limits**: Respects rate limits of all external APIs
- **Memory Usage**: Optimized for minimal memory footprint
- **Concurrent Users**: Supports multiple users simultaneously
- **Uptime**: Designed for 24/7 operation with auto-recovery

## 🔒 Security

- **API Key Protection**: Environment variables recommended
- **Input Validation**: All user inputs are sanitized
- **Error Handling**: No sensitive information leaked in error messages
- **Rate Limiting**: Built-in protection against spam
- **Data Privacy**: No user data stored permanently

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Ensure backward compatibility
- Test with multiple stock symbols

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/telegram-stock-analyst-bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/telegram-stock-analyst-bot/discussions)
- **Wiki**: [Project Wiki](https://github.com/yourusername/telegram-stock-analyst-bot/wiki)

## 📊 Roadmap

- [ ] **Cryptocurrency Support** - Add crypto price tracking
- [ ] **Portfolio Tracking** - User portfolio management
- [ ] **Price Alerts** - Custom price notifications  
- [ ] **Technical Indicators** - RSI, MACD, Bollinger Bands
- [ ] **News Integration** - Financial news correlation
- [ ] **Multi-language Support** - International markets
- [ ] **Web Dashboard** - Companion web interface
- [ ] **Mobile App** - Native mobile application

## 🙏 Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com) for financial data
- [Perplexity AI](https://www.perplexity.ai) for market analysis
- [Telegram Bot API](https://core.telegram.org/bots/api) for bot framework
- [Python Telegram Bot](https://python-telegram-bot.org/) library
- [Matplotlib](https://matplotlib.org/) for chart generation

## ⭐ Show Your Support

If this project helped you, please give it a ⭐ on GitHub!

## 📞 Contact

- **Developer**: Your Name
- **Email**: your.email@example.com
- **Telegram**: [@yourusername](https://t.me/yourusername)
- **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/yourusername)

---

<div align="center">
  <b>Made with ❤️ for the trading community</b>
</div>
