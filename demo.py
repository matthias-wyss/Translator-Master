"""
Simple bot to respond to different kinds of messages.

```python
python demo.py
```

Press Ctrl-C on the command line to stop the bot.
"""

import logging

from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from keys import TELEGRAM_KEY

from PIL import Image
import numpy as np
import audiofile
from pdfrw import PdfReader
from text_to_text import text_to_text
from detect_language import detect_language

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TEXT, LANGUAGEOUT = range(2)

conversion = {'DE': 'de_DE', 'FR': 'fr_XX', 'EN': 'en_XX', 'IT': 'it_IT'}
translation = {'text' : None, 'language': None}

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


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo user photo."""
    photo_file = await update.message.photo[-1].get_file()

    # load image into numpy array
    tmp_photo = "tmp_photo.jpg"
    await photo_file.download_to_drive(tmp_photo)
    img = np.array(Image.open(tmp_photo))

    # respond photo
    await update.message.reply_photo(tmp_photo, caption=f"Image shape: {img.shape}")


async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo user audio."""

    audio_file = await update.message.voice.get_file()

    # load audio into numpy array
    tmp_file = "voice_note.ogg"
    await audio_file.download_to_drive(tmp_file)

    signal, sampling_rate = audiofile.read(tmp_file, always_2d=True)
    duration = signal.shape[1] / sampling_rate

    # respond audio
    await update.message.reply_voice(tmp_file, caption=f"Voice note duration: {duration} seconds")


async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo user audio."""

    audio_file = await update.message.audio.get_file()


    # load audio into numpy array
    tmp_file = "audio.wav"
    await audio_file.download_to_drive(tmp_file)

    signal, sampling_rate = audiofile.read(tmp_file, always_2d=True)
    duration = signal.shape[1] / sampling_rate

    # respond audio
    await update.message.reply_audio(tmp_file, caption=f"Audio duration: {duration} seconds")


async def attachment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo user attachment."""

    attachment_file = await update.message.document.get_file()

    # download pdf and send back
    tmp_file = "attachment.pdf"
    await attachment_file.download_to_drive(tmp_file)

    # read PDF
    reader = PdfReader(tmp_file)

    # get title and number of pagers
    title = reader.Info.Title
    num_pages = len(reader.pages)

    # respond attachment
    await update.message.reply_document(tmp_file, caption=f"PDF title: {title}, number of pages: {num_pages}")


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False

    for job in current_jobs:
        job.schedule_removal()

    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id

    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)
        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /timer <seconds>")


async def how_are_you(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Select from randomly from set responses."""
    responses = ["Fine", "Good", "Bad", "So so"]
    await update.message.reply_text(np.random.choice(responses))
    
async def text2text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Insert text",
        reply_markup=ReplyKeyboardRemove(),
    )
    return TEXT
    
async def ask_text(update: Update, context: ContextTypes.DEFAULT_TYPE)-> int :
    user = update.message.from_user
    logger.info("text of %s: %s", user.first_name, update.message.text)
    translation['text'] = update.message.text
    reply_keyboard = [["FR", "EN", "DE", "IT"]]
    await update.message.reply_text(
        "In what language do you want to translate your text",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Language ?"
        ),)
    return LANGUAGEOUT
    
async def ask_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user = update.message.from_user
    logger.info("language of %s: %s", user.first_name, update.message.text)
    translation['language'] = conversion[update.message.text]
    language_in = conversion[detect_language(translation['text'])[0].upper()]
    text_translated = text_to_text(translation['text'], language_in, translation['language'])
    await update.message.reply_text(text_translated)
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
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_KEY).build()


    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # menu commands
    application.add_handler(CommandHandler("timer", set_timer))
    application.add_handler(CommandHandler("howareyou", how_are_you))

    # on non command i.e message - echo the message on Telegram
    #application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # photo input
    application.add_handler(
        MessageHandler(filters.PHOTO & ~filters.COMMAND, photo, block=True)
    )

    # voice input
    application.add_handler(
        MessageHandler(filters.VOICE & ~filters.COMMAND, voice, block=True)
    )

    # audio input
    application.add_handler(
        MessageHandler(filters.AUDIO & ~filters.COMMAND, audio, block=True)
    )

    # attachments
    application.add_handler(
        MessageHandler(filters.ATTACHMENT & ~filters.COMMAND, attachment, block=True)
    )
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("text2text", text2text)],
        states={
            TEXT: [MessageHandler(filters.TEXT, ask_text)],
            LANGUAGEOUT: [MessageHandler(filters.Regex("^(FR|EN|DE|IT)$"), ask_language)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    

if __name__ == "__main__":
    main()
    
    