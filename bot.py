from custom_libs import utils
from custom_libs import db
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

db_folder = "db_telegram_bot"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Stars", "Feeling", "All"]]

    await update.message.reply_text(
        "Chose operation",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Stars, Feeling or All"
        ),
    )

    return CHOSE


async def operation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Commento."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Now, send me your location please, or send /skip if you don't want to."
    )

    chat_id = update.message.chat_id
    chose = update.message.text

    # save the chose in a json
    with open(f"{db_folder}/chose_{chat_id}.json", "w") as outfile:
        json.dump({"chose": chose}, outfile)

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Commento."""
    user = update.message.from_user
    user_location = update.message.location

    latitude = user_location.latitude
    longitude = user_location.longitude
    chat_id = update.message.chat_id

    with open(f"{db_folder}/location_{chat_id}.json", "w") as outfile:
        json.dump({"latitude": latitude, "longitude": longitude}, outfile)

    await update.message.reply_text("Write max distance")

    return RADIUS


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Commento."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text("You seem a bit paranoid!")

    return RADIUS


async def radius(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Commento."""
    max_distance = 0

    try:
        max_distance = int(update.message.text)
    except:
        await update.message.reply_text("Error: wrong format")
        return ConversationHandler.END

    chat_id = update.message.chat_id
    with open(f"{db_folder}/location_{chat_id}.json", "r") as infile:
        user_location = json.load(infile)

    with open(f"{db_folder}/chose_{chat_id}.json", "r") as infile:
        chose = json.load(infile)["chose"]

    current_position = [user_location["latitude"], user_location["longitude"]]

    df = db.get_dataset('McDonald_s_Reviews_preprocessed')

    if chose == "Stars" or chose == "All":
        try:
            best_restaurant = utils.select_best_restaurant_from_stars(
                df, current_position, max_distance)
            lat = best_restaurant['latitude'].values[0]
            long = best_restaurant['longitude'].values[0]
            await update.message.reply_location(latitude=lat, longitude=long)
            await update.message.reply_text("Best rating adders: " + best_restaurant['store_address'].values[0])
        except Exception as e:
            await update.message.reply_text(str(e))

    if chose == "Feeling" or chose == "All":
        try:
            best_restaurant = utils.select_best_restaurant_from_sentiment(
                df, current_position, max_distance, sentiment_column='sentiment_auto')
            lat = best_restaurant['latitude'].values[0]
            long = best_restaurant['longitude'].values[0]
            await update.message.reply_location(latitude=lat, longitude=long)
            await update.message.reply_text("Best rating adders: " + best_restaurant['store_address'].values[0])
        except Exception as e:
            await update.message.reply_text(str(e))

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
