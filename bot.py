
# pip install python-telegram-bot --upgrade

import logging

from telegram import __version__ as TG_VER
from custom_libs import utils

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text

    try:
        current_position = [float(user_text.split(",")[0]), float(user_text.split(",")[1])]
        max_distance = int(user_text.split(",")[2])
    except:
        await update.message.reply_text("Error: wrong format")
        return
    
    best_rated_result = utils.best_restaurant_from_stars_reply(current_position, max_distance)
    best_feeling_result = utils.best_restaurant_from_sentiment_reply(current_position, max_distance, sentiment_column='sentiment_auto')

    # Stelline
    await update.message.reply_text("Best rating: " + best_rated_result)

    # Sentiment sul dataset di partenza
    await update.message.reply_text("Best feeling: " + best_feeling_result)


# Define a location handler
async def location(update, context):
    # Get the latitude and longitude from the message
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    

    # Send the latitude and longitude as a reply
    await update.message.reply_text(f'Latitude: {latitude}, Longitude: {longitude}')


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6366438224:AAE_s84P3k9yCd96OIHIz6aTlS7A3vRNTvI").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_user))

    # Register the location handler
    location_handler = MessageHandler(filters.LOCATION, location)
    application.add_handler(location_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()