# pip install python-telegram-bot --upgrade
from custom_libs import utils
import json

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOSE, LOCATION, RADIUS = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Stars", "Feeling", "All"]]

    await update.message.reply_text(
        "Chose operation",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Chose"
        ),
    )

    return CHOSE


async def operation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Now, send me your location please, or send /skip if you don't want to."
    )

    chat_id = update.message.chat_id
    chose = update.message.text

    # save the chose in a json
    with open(f"chose_{chat_id}.json", "w") as outfile:
        json.dump({"chose": chose}, outfile)

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location

    latitude = user_location.latitude
    longitude = user_location.longitude
    chat_id = update.message.chat_id

    # create a json file with the user's location
    with open(f"location_{chat_id}.json", "w") as outfile:
        json.dump({"latitude": latitude, "longitude": longitude}, outfile)

    await update.message.reply_text(
        "Write max distance"
    )

    return RADIUS


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return RADIUS


async def radius(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    # logger.info("Bio of %s: %s", user.first_name, update.message.text)

    max_distance = 0
    try:
        max_distance = int(update.message.text)
    except:
        await update.message.reply_text("Error: wrong format")
        return ConversationHandler.END

    chat_id = update.message.chat_id
    with open(f"location_{chat_id}.json", "r") as infile:
        user_location = json.load(infile)

    current_position = [user_location["latitude"], user_location["longitude"]]

    best_rated_result = utils.best_restaurant_from_stars_reply(
        current_position, max_distance)
    best_feeling_result = utils.best_restaurant_from_sentiment_reply(
        current_position, max_distance, sentiment_column='sentiment_auto')

    with open(f"chose_{chat_id}.json", "r") as infile:
        chose = json.load(infile)["chose"]

    if chose == "Stars":
        await update.message.reply_text("Best rating: " + best_rated_result)
    elif chose == "Feeling":
        await update.message.reply_text("Best feeling: " + best_feeling_result)
    else:
        await update.message.reply_text("Best rating: " + best_rated_result)
        await update.message.reply_text("Best feeling: " + best_feeling_result)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(
        "6366438224:AAE_s84P3k9yCd96OIHIz6aTlS7A3vRNTvI").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOSE: [MessageHandler(filters.Regex("^(Stars|Feeling|All)$"), operation)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
                CommandHandler("skip", skip_location),
            ],
            RADIUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, radius)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
