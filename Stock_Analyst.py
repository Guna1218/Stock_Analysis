"""python Stock_Analyst.py"""

import os
import asyncio
import logging
import requests
import json
import re
from datetime import datetime
from typing import Dict, Optional, Any


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration - CREDENTIALS
TELEGRAM_BOT_TOKEN = "8070819148:AAGgWiBPYGGtuK9SR9XwoJX4*******A6IQ"      
PERPLEXITY_API_KEY = "pplx-GGMnWV0oHSspCius79TzRifuGqIsuIzyAJFwF*******DBP9"
CHART_IMG_API_KEY = "Q4M6O41Olo1WJwKkHSrye3DpsKARfjjd8wUTgjIX"

class TelegramStockAnalyst:
    def __init__(self):
        self.user_sessions = {}  # Store user conversation (memory)
        self.perplexity_base_url = "https://api.perplexity.ai/chat/completions"

    def extract_stock_ticker(self, text: str) -> Optional[str]:
        """Extract stock ticker from message text"""
        
        text_upper = text.upper()

        
        patterns = [
            r'\b([A-Z]{2,5})\b',  # Simple ticker pattern
            r'\$([A-Z]{2,5})\b',  # With $ prefix
            r'TICKER:?\s*([A-Z]{2,5})',  # Explicit ticker mention
            r'ANALYZE\s+([A-Z]{2,5})',  # "analyze AAPL"
            r'STOCK\s+([A-Z]{2,5})',   # "stock AAPL"
        ]

        # Words that aren't tickers
        common_words = {
            'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 
            'WAS', 'ONE', 'OUR', 'HAD', 'BUT', 'WORD', 'EACH', 'WHICH', 'THEIR', 
            'TIME', 'WILL', 'ABOUT', 'WOULD', 'THERE', 'COULD', 'OTHER', 'WHAT',
            'YOUR', 'HOW', 'NOW', 'GET', 'HAS', 'HIS', 'MAY', 'NEW', 'WAY', 'WHO'
        }

        for pattern in patterns:
            matches = re.findall(pattern, text_upper)
            for match in matches:
                if match not in common_words and len(match) >= 2:
                    return match

        return None

    async def get_stock_chart_url(self, ticker: str) -> Optional[str]:
        """Get stock chart URL from Chart-img API"""
        try:
            url = "https://api.chart-img.com/v2/tradingview/advanced-chart"
            params = {
                'symbol': ticker.upper(),
                'interval': '1D',
                'studies': 'MACD@tv-basicstudies,RSI@tv-basicstudies,BB@tv-basicstudies',
                'theme': 'dark',
                'width': '800',
                'height': '600'
            }

            headers = {}
            if CHART_IMG_API_KEY != "Q4M6O41Olo1WJwKkHSrye3DpsKARfjjd8wUTgjIX":
                headers['X-API-KEY'] = CHART_IMG_API_KEY

            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('url')
            else:
                logger.warning(f"Chart API returned status {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error getting chart: {e}")
            return None

    async def analyze_with_perplexity(self, ticker: str, user_message: str, chart_url: Optional[str] = None) -> str:
        """Analyze stock using Perplexity AI API"""
        try:
            # Prompt for ChatBot
            prompt = f"""You are a professional financial analyst. Analyze the stock {ticker} based on this user request:

User Message: {user_message}

Please provide a comprehensive but concise analysis including:
1. **Company Overview**: Brief description of the company and sector
2. **Market Context**: Current market conditions affecting this stock  
3. **Technical Analysis**: Key technical levels and trends
4. **Fundamental Factors**: Key business metrics and recent news impact
5. **Risk Assessment**: Main risks and considerations
6. **Educational Insights**: Learning points about this stock/sector

Format your response professionally but conversationally, suitable for Telegram messaging.

IMPORTANT: 
- Do not provide explicit buy/sell recommendations
- Focus on educational analysis
- Keep responses under 1000 characters for Telegram readability
- Use emojis sparingly for better formatting
- Include current market data and recent news
"""

            if chart_url:
                prompt += f"\n\nChart URL for reference: {chart_url}"

            # Call API
            response = await self._call_perplexity_api(prompt)
            return response

        except Exception as e:
            logger.error(f"Perplexity Analysis error: {e}")
            return f"🤖 AI analysis temporarily unavailable. Error: {str(e)}"

    async def _call_perplexity_api(self, prompt: str) -> str:
        """Call Perplexity AI API"""
        if PERPLEXITY_API_KEY == "YOUR_PERPLEXITY_API_KEY":
            return "⚠️ Perplexity API key not configured. Please add your API key."

        headers = {
            'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
            'Content-Type': 'application/json'
        }

        # Using sonar-pro model 
        data = {
            'model': 'sonar-pro',
            'messages': [
                {
                    'role': 'system', 
                    'content': 'You are a financial analyst providing educational stock analysis. Be precise, concise, and cite sources when possible.'
                },
                {
                    'role': 'user', 
                    'content': prompt
                }
            ],
            'max_tokens': 1000,
            'temperature': 0.2,
            'search_recency_filter': 'week',  # Focus on recent information
            'return_images': False,
            'return_related_questions': False
        }

        try:
            response = requests.post(
                self.perplexity_base_url,
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']

                # Add citations if available
                if 'search_results' in result and result['search_results']:
                    citations = "\n\n📚 Sources:\n"
                    for i, source in enumerate(result['search_results'][:3], 1):  # Limit to 3 sources
                        citations += f"{i}. {source.get('title', 'Unknown')}\n"
                    content += citations

                return content
            else:
                error_msg = f"Perplexity API error: {response.status_code}"
                if response.text:
                    error_details = response.json().get('error', {}).get('message', 'Unknown error')
                    error_msg += f" - {error_details}"
                raise Exception(error_msg)

        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON decode error: {str(e)}")


bot_instance = TelegramStockAnalyst()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = """
🤖 **Welcome to Stock Analyst Bot!**

I can help you analyze stocks and provide technical insights powered by Perplexity AI. Here's how to use me:

📊 **Commands:**
• Send any message mentioning a stock ticker (e.g., "analyze AAPL")
• Use $ prefix: "What about $TSLA?"
• Direct format: "MSFT analysis please"

💡 **Features:**
• Real-time market data via Perplexity AI
• Technical chart analysis
• AI-powered insights with citations
• Educational explanations
• Risk assessments

⚠️ **Disclaimer:** 
This bot provides educational analysis only. Not financial advice.

Try asking: "Analyze AAPL" or "What's happening with $TSLA?"
"""

    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🔧 **How to use Stock Analyst Bot:**

**Stock Analysis:**
• "Analyze AAPL" - Get full analysis
• "Chart for TSLA" - Focus on technical analysis  
• "$MSFT overview" - Company overview
• "NVDA vs AMD" - Compare stocks

**Supported Features:**
✅ Real-time chart generation
✅ Perplexity AI-powered analysis
✅ Current market data with citations  
✅ Technical indicator analysis
✅ Risk assessment
✅ Educational explanations

**Tips:**
• Use clear stock ticker symbols (2-5 letters)
• Ask specific questions for better responses
• Try different analysis angles

Need help? Just ask about any stock!
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    user_id = update.effective_user.id
    user_message = update.message.text
    chat_id = update.effective_chat.id

    
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    
    ticker = bot_instance.extract_stock_ticker(user_message)

    if not ticker:
        
        response = """
🤔 I didn't detect a stock ticker in your message.

Try mentioning a stock like:
• "Analyze AAPL"
• "What about $TSLA?"  
• "MSFT analysis please"

Or use /help for more examples!
"""
        await update.message.reply_text(response)
        return

    
    await update.message.reply_text(f"🔍 Analyzing {ticker} ... Please wait...")

    try:
        
        chart_url = await bot_instance.get_stock_chart_url(ticker)

        
        analysis = await bot_instance.analyze_with_perplexity(ticker, user_message, chart_url)

        
        response = f"""
📈 **Analysis for {ticker}**

{analysis}

"""

        if chart_url:
            response += f"📊 [View Chart]({chart_url})\n\n"

        response += "⚠️ *Educational purposes only. Not financial advice.*"

        
        await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=False)

        
        if user_id not in bot_instance.user_sessions:
            bot_instance.user_sessions[user_id] = []

        bot_instance.user_sessions[user_id].append({
            'ticker': ticker,
            'analysis': analysis,
            'timestamp': datetime.now()
        })

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(
            "❌ Sorry, I encountered an error analyzing that stock. Please try again later."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print("❌ Please set your Telegram Bot Token in the script")
        return

    if PERPLEXITY_API_KEY == "YOUR_PERPLEXITY_API_KEY":
        print("❌ Please set your Perplexity API Key in the script")
        print("📝 Get your API key from: https://www.perplexity.ai/settings/api")
        return

    print("🤖 Starting Telegram Stock Analyst Bot with Perplexity AI...")

    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    
    app.add_error_handler(error_handler)

    
    print("✅ Bot is running... Press Ctrl+C to stop")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    
    main()
