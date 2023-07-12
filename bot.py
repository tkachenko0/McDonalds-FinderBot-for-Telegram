import json
import logging
from custom_libs import db
from custom_libs import best_restaurants as br
from telegram import __version__ as TG_VER

try: from telegram import __version_info__
except ImportError: __version_info__ = (0, 0, 0, 0, 0) 

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

CHOSE, LOCATION, RADIUS = range(3)

db_folder = "db_telegram_bot"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Stars", "Feeling", "Both"]]
    start_mess = f"Hi, chose if you wish to locate the best-rated MC or the one with the best emotion and feeling experience. You can choose to find both as well."
    await update.message.reply_text(start_mess, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder=""))
    return CHOSE


async def operation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Now, send me your location please, or send /skip if you don't want to.")

    chat_id = update.message.chat_id
    chose = update.message.text

    with open(f"{db_folder}/chose_{chat_id}.json", "w") as outfile:
        json.dump({"chose": chose}, outfile)

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_location = update.message.location
    latitude = user_location.latitude
    longitude = user_location.longitude
    chat_id = update.message.chat_id

    with open(f"{db_folder}/location_{chat_id}.json", "w") as outfile:
        json.dump({"latitude": latitude, "longitude": longitude}, outfile)

    await update.message.reply_text("Write max distance in km from your position to find the best restaurant.")

    return RADIUS


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("You seem a bit paranoid!")
    return RADIUS


async def radius(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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

    if chose == "Stars" or chose == "Both":
        try:
            best_restaurant = br.select_best_restaurant_from_stars(df, current_position, max_distance)
            await update.message.reply_text("Best ⭐ rated restaurant's address: " + best_restaurant['store_address'].values[0])
            lat, long = best_restaurant['latitude'].values[0], best_restaurant['longitude'].values[0]
            await update.message.reply_location(latitude=lat, longitude=long)
            await update.message.reply_photo(photo=open('bot_images/mc1.jpg', 'rb'))
            return ConversationHandler.END
        except Exception as e:
            await update.message.reply_text(str(e))
            await update.message.reply_photo(photo=open('bot_images/404.gif', 'rb'))
            return ConversationHandler.END

    if chose == "Feeling" or chose == "Both":
        try:
            best_restaurant = br.select_best_restaurant_from_sentiment(df, current_position, max_distance, sentiment_column='sentiment_auto')
            await update.message.reply_text("Best 💫 feeling restaurant's address: " + best_restaurant['store_address'].values[0])
            lat, long = best_restaurant['latitude'].values[0], best_restaurant['longitude'].values[0]
            await update.message.reply_location(latitude=lat, longitude=long)
            await update.message.reply_photo(photo=open('bot_images/mc2.jpg', 'rb'))
            return ConversationHandler.END
        except Exception as e:
            await update.message.reply_text(str(e))
            await update.message.reply_photo(photo=open('bot_images/404.gif', 'rb'))
            return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    bye_mess = "Bye! I hope we can talk again some day."
    await update.message.reply_text(bye_mess, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token("6313189469:AAHsJw9c4M_HHoMgrrQ8zNjfi7oYYgeVAO4").build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOSE: [MessageHandler(filters.Regex("^(Stars|Feeling|Both)$"), operation)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
                CommandHandler("skip", skip_location),
            ],
            RADIUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, radius)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
