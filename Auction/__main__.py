import logging
from telegram.ext import Application
from config import BOT_TOKEN
from Auction.Modules import start, tag, stoptag, ping, help, bcast

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Register all handlers
    start.register(application)
    tag.register(application)
    stoptag.register(application)
    ping.register(application)
    help.register(application)
    bcast.register(application)
            
    print("🚀 Aho Tagall Bot Started!")
    application.run_polling()

if __name__ == "__main__":
    main()