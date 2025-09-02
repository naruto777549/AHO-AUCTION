# Auction/main.py
import logging
from Auction import app

# Import all modules
from Auction.Modules import start, tag, stoptag, help, bcast, ping

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO
)

if __name__ == "__main__":
    app.run()