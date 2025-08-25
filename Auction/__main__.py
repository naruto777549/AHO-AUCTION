import logging
from telegram.ext import Application
from AlphaWaifu.config import BOT_TOKEN
from AlphaWaifu.Modules import start, upload, guess, changetime, drop, fdrop, reset, check 

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Register all handlers
    start.register(application)
    upload.register(application)
    guess.register(application)
    changetime.register(application)
    drop.register(application)
    fdrop.register(application)
    reset.register(application)
    check.register(application)
        
    print("🚀 AlphaWaifu Bot Started!")
    application.run_polling()

if __name__ == "__main__":
    main()