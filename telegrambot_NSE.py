import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def get_top_movers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # URLs for top gainers and losers
        gainers_url = "https://www.nseindia.com/market-data/top-gainers-losers"
        

        # Fetch HTML content
        response = requests.get(gainers_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract top gainers and losers
        gainers_table = soup.find('table', {'id': 'topGainers'})
        losers_table = soup.find('table', {'id': 'topLosers'})

        if gainers_table and losers_table:
            # Extract data from tables (first 5 rows only)
            gainers_rows = gainers_table.find_all('tr')[1:6]
            losers_rows = losers_table.find_all('tr')[1:6]

            gainers_data = []
            for row in gainers_rows:
                cols = row.find_all('td')
                gainers_data.append({'Symbol': cols[0].text, 'LTP': cols[1].text, 'Change %': cols[4].text})
            gainers_table = tabulate(gainers_data, headers="keys", tablefmt='simple')

            losers_data = []
            for row in losers_rows:
                cols = row.find_all('td')
                losers_data.append({'Symbol': cols[0].text, 'LTP': cols[1].text, 'Change %': cols[4].text})
            losers_table = tabulate(losers_data, headers="keys", tablefmt='simple')

            # Send messages
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"**Top 5 Gainers:**\n\n`\n{gainers_table}\n`", parse_mode="Markdown")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"**Top 5 Losers:**\n\n`\n{losers_table}\n`", parse_mode="Markdown")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Error: Unable to find gainers/losers tables on NSE website.")

    except requests.RequestException as e:
        logging.error(f"Error fetching NSE data: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while fetching data.")

# ... (help_command and rest of the code remains the same)


# Help command (unchanged)
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Available commands:\n/topmovers - Get top gainers and losers from NSE\n/help - Show this help message"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

if __name__ == '__main__':
    application = ApplicationBuilder().token('6709242892:AAE96KVSuKfw3ZiCLcCfZgmfSeEmoCbEQyQ').build()  

    top_movers_handler = CommandHandler("topmovers", get_top_movers)
    help_handler = CommandHandler("help", help_command)

    application.add_handler(top_movers_handler)
    application.add_handler(help_handler)

    application.run_polling()

