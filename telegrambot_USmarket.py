import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

FINNHUB_API_KEY = 'cp6prrhr01qm8p9l69l0cp6prrhr01qm8p9l69lg'  # Replace with your actual Finnhub API key

async def get_stock_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            raise ValueError("Please provide a stock symbol (e.g., /price AAPL)")

        symbol = context.args[0].upper()
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if "c" in data and data["c"] is not None:
            price = data["c"]
            message = f"Current price for {symbol}: {price:.2f}"
        else:
            message = f"Price for {symbol} not available."

        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    except (ValueError, requests.RequestException) as e:
        logging.error(f"Error fetching stock data: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while fetching stock data.")

# Help command (unchanged)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Available commands:\n/price <symbol> - Get the current price of a stock (e.g., /price AAPL)\n/help - Show this help message"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

if __name__ == '__main__':
    application = ApplicationBuilder().token('6709242892:AAE96KVSuKfw3ZiCLcCfZgmfSeEmoCbEQyQ').build()

    stock_price_handler = CommandHandler("price", get_stock_price)
    help_handler = CommandHandler("help", help_command)

    application.add_handler(stock_price_handler)
    application.add_handler(help_handler)

    application.run_polling()

