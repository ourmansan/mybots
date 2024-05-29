import logging
import csv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from nsepython import nse_get_top_gainers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def get_top_gainers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        top_gainers_list = nse_get_top_gainers()

        # Create CSV file
        with open("top_gainers.csv", "w", newline="") as csvfile:
            fieldnames = ['symbol', 'open', 'high', 'low', 'ltp', 'ptsC', 'per', 'trdVol', 'ntP', 'mVal']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(top_gainers_list)  # Write the list of dictionaries directly

        # Send CSV file to Telegram
        with open("top_gainers.csv", "rb") as csvfile:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=csvfile, filename="top_gainers.csv")

    except Exception as e:
        logging.error(f"Error fetching or sending NSE data: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while processing the data.")


# Help command (unchanged)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Available commands:\n/topgainers - Get top gainers from NSE\n/help - Show this help message"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

if __name__ == '__main__':
    application = ApplicationBuilder().token('6709242892:AAE96KVSuKfw3ZiCLcCfZgmfSeEmoCbEQyQ').build()

    top_gainers_handler = CommandHandler("topgainers", get_top_gainers_command) 
    help_handler = CommandHandler("help", help_command)

    application.add_handler(top_gainers_handler)
    application.add_handler(help_handler)

    application.run_polling()

