from os import getenv
from os.path import splitext
import logging
from pathlib import Path
from random import choice

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    # MessageHandler,
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

logger.info("booting up: loading main.py")


TELEGRAM_MSG_LENGTH = 4096


def pick_file(directory: str) -> str:
    """returns a random chosen filename from a folder"""
    filenames = list(Path(directory).rglob("*.*"))

    return choice(filenames).name


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = [
        "a one-percenter-helper.",
        "ask me about the pies",
        "or the gramp's fries",
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="\n".join(text),
    )

    logger.debug(
        f"start: {update.effective_chat.id} - {update.effective_chat.effective_name}"
    )


async def pie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("assets/pie.jpg", "rb") as file:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file)

    logger.debug(
        f"got pied in {update.effective_chat.id} - {update.effective_chat.effective_name}"
    )


async def pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(
        f"asked for a pic in {update.effective_chat.id} - {update.effective_chat.effective_name}"
    )

    directory = "assets/pics/"
    filename = pick_file(directory)
    full_path = directory + filename

    logger.debug(f"pic: picked {filename}")
    with open(full_path, "rb") as file:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=file,
            caption=full_path,
        )

    logger.debug("pic sent!")


async def ded(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(
        f"got ded'ed in {update.effective_chat.id} - {update.effective_chat.effective_name}"
    )

    directory = "assets/ded/"
    filename = pick_file(directory=directory)
    full_path = directory + filename

    logger.debug(f"ded's file {filename} chosen")

    if splitext(filename)[1] == ".txt":
        with open(full_path, "r") as file:
            contents = file.read()
            for i in range(0, len(contents), TELEGRAM_MSG_LENGTH):
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=contents[i : i + TELEGRAM_MSG_LENGTH],
                    parse_mode="HTML",
                )
            logger.debug("ded's copypasta sent!")
    else:
        with open(full_path, "rb") as file:
            try:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=file,
                )
                logger.debug("screenshot of ded's msg sent!")
            except Exception as e:
                logger.error(f"tried to send photo {filename} but failed; not a photo?")
                logger.error(e)


if __name__ == "__main__":
    logger.debug("starting up...")
    TG_TOKEN = getenv("TG_TOKEN")
    if not TG_TOKEN:
        logger.fatal("no TG_TOKEN!")
        raise ValueError("no TG_TOKEN!")
    logger.debug("TG_TOKEN loaded")

    app = ApplicationBuilder().token(TG_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pie", pie))
    app.add_handler(CommandHandler("ded", ded))
    app.add_handler(CommandHandler("pic", pic))
    # app.add_handler(MessageHandler())

    logger.info("starting polling...")
    app.run_polling()
