from os import getenv, walk
from os.path import splitext
import logging
from random import choice
from asyncio import run

from telegram import Update
from telegram.constants import MessageLimit
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    # MessageHandler,
    ContextTypes,
)

formatter = logging.Formatter("%(asctime)s - %(name)s - [%(levelname)s] > %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stderr_log_handler = logging.StreamHandler()
stderr_log_handler.setFormatter(formatter)

file_log_handler = logging.FileHandler("backend.log")
file_log_handler.setFormatter(formatter)

logger.addHandler(stderr_log_handler)
logger.addHandler(file_log_handler)

logger.info("booting up: loading main.py")


def pick_file(directory: str) -> str:
    """returns a random chosen filename from a folder; recursive"""

    fullpath_filenames = []
    for path, _, local_filenames in walk(directory):
        fullpath_filenames.extend([path + file for file in local_filenames])

    return choice(fullpath_filenames)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = [
        "a one-percenter-helper.",
        "ask me about the pies,",
        "the gramp's fries,",
        "or for a picture for good times,",
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

    logger.debug(f"pic: picked {filename}")
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=filename,
        caption=filename,
    )

    logger.debug("pic sent!")


async def send_text(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    filepath: str,
) -> None:
    with open(filepath, "r") as file:
        text = file.read()
    for i in range(0, len(text), MessageLimit.MAX_TEXT_LENGTH):
        await context.bot.send_message(
            chat_id=chat_id,
            text=text[i : i + MessageLimit.MAX_TEXT_LENGTH],
            parse_mode="HTML",
        )


async def ded(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug(
        f"got ded'ed in {update.effective_chat.id} - {update.effective_chat.effective_name}"
    )

    directory = "assets/ded/"
    filename = pick_file(directory=directory)

    logger.debug(f"ded's file {filename} chosen")

    file_extension = splitext(filename)[1]

    if file_extension == ".txt":
        # ded's copypasta, in text format (maybe w/ html layout tags)
        # ? using a wrapper to paginate
        await send_text(
            context=context,
            chat_id=update.effective_chat.id,
            filepath=filename,
        )
        logger.debug("ded's copypasta sent!")

    if file_extension == ".ogg":
        # voice recording
        await context.bot.send_voice(
            chat_id=update.effective_chat.id,
            voice=filename,
        )
        logger.debug("sent a ded-related voice message!")
        # except Exception as e:
        #     logger.error(f"tried to send photo {filename} but failed; not a photo?")
        #     logger.error(e)

    if file_extension == ".jpg":
        # shitpost pic
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=filename,
        )
        logger.debug("screenshot of ded's msg sent!")
        # except Exception as e:
        #     logger.error(f"tried to send photo {filename} but failed; not a photo?")
        #     logger.error(e)


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

    # todo: add tg logging
    # logger.addHandler()

    logger.info("starting polling...")
    app.run_polling()
