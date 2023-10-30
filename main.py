from os import getenv
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

formatter = logging.Formatter("%(asctime)s - %(name)s - [%(levelname)s]:%(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stderr_log_handler = logging.StreamHandler()
stderr_log_handler.setFormatter(formatter)

file_log_handler = logging.FileHandler("backend.log")
file_log_handler.setFormatter(formatter)

logger.addHandler(stderr_log_handler)
logger.addHandler(file_log_handler)

logger.info("booting up")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = [
        "a one-percenter-helper.",
        "ask me about the pies!",
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="\n".join(text),
    )

    logger.debug(
        f"start: {update.effective_chat.id} - {update.effective_chat.full_name}"
    )


async def pie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("assets/pie.jpg", "rb") as file:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file)

    logger.debug(
        f"got pied in {update.effective_chat.id} - {update.effective_chat.full_name}"
    )


if __name__ == "__main__":
    TG_TOKEN = getenv("TG_TOKEN")
    if not TG_TOKEN:
        logger.fatal("no TG_TOKEN!")
        raise ValueError("no TG_TOKEN!")

    app = ApplicationBuilder().token(TG_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pie", pie))

    logger.info("starting polling...")
    app.run_polling()
