import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram.ext import CallbackContext
from datetime import datetime, timedelta
import time

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# API Keys and other configuration
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))
FILE_STORE_CHANNEL = int(os.getenv('FILE_STORE_CHANNEL'))
LOG_CHANNEL = int(os.getenv('LOG_CHANNEL'))

# File deletion time (in minutes)
delete_time = None

# Start Command
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    if user.id == OWNER_ID:
        keyboard = [
            [InlineKeyboardButton("Get Link", callback_data='getlink')],
            [InlineKeyboardButton("Batch", callback_data='batch')],
            [InlineKeyboardButton("Custom Batch", callback_data='custom_batch')],
            [InlineKeyboardButton("Settings", callback_data='setting')],
            [InlineKeyboardButton("Delete Links", callback_data='delete')],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("Generate Link", callback_data='generate')]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome to the bot! Choose an option:', reply_markup=reply_markup)

# Generate Link Command
def getlink(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    keyboard = [
        [InlineKeyboardButton("One File Store", callback_data='onefile')],
        [InlineKeyboardButton("Multiple File Store", callback_data='multiplefile')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Choose an option for file storage:", reply_markup=reply_markup)

# One File Storage
def onefile(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    # Logic for storing one file
    query.edit_message_text(text="Send me the file to store.")

# Multiple Files Storage
def multiplefile(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # Logic for storing multiple files
    query.edit_message_text(text="Send me multiple files to store.")

# Delete File Command
def delete(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # Deleting a specific file using the link
    query.edit_message_text(text="Please provide the link to delete the file.")

# Settings Command
def setting(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Automatic Delete", callback_data='auto_delete')],
        [InlineKeyboardButton("File Protect", callback_data='file_protect')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Choose settings:", reply_markup=reply_markup)

# Automatic Delete Time
def auto_delete(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("30 Minutes", callback_data='30min')],
        [InlineKeyboardButton("1 Hour", callback_data='1hour')],
        [InlineKeyboardButton("3 Hours", callback_data='3hours')],
        [InlineKeyboardButton("10 Hours", callback_data='10hours')],
        [InlineKeyboardButton("1 Day", callback_data='1day')],
        [InlineKeyboardButton("OFF", callback_data='off')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Set file delete time:", reply_markup=reply_markup)

# File Protect
def file_protect(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("ON", callback_data='protect_on')],
        [InlineKeyboardButton("OFF", callback_data='protect_off')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="File Protect Settings:", reply_markup=reply_markup)

# Handler Functions for Specific Actions
def set_delete_time(update: Update, context: CallbackContext):
    global delete_time
    query = update.callback_query
    query.answer()
    
    # Set the delete time based on the selection
    if query.data == '30min':
        delete_time = timedelta(minutes=30)
    elif query.data == '1hour':
        delete_time = timedelta(hours=1)
    elif query.data == '3hours':
        delete_time = timedelta(hours=3)
    elif query.data == '10hours':
        delete_time = timedelta(hours=10)
    elif query.data == '1day':
        delete_time = timedelta(days=1)
    elif query.data == 'off':
        delete_time = None

    query.edit_message_text(text=f"File delete time set to: {query.data}")

# Protect File Actions
def protect_file(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == 'protect_on':
        # Logic to protect files from being forwarded
        query.edit_message_text(text="File protection is ON.")
    elif query.data == 'protect_off':
        # Logic to unprotect files from being forwarded
        query.edit_message_text(text="File protection is OFF.")

# Main function to run the bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("getlink", getlink))
    dispatcher.add_handler(CommandHandler("setting", setting))
    dispatcher.add_handler(CommandHandler("delete", delete))
    
    dispatcher.add_handler(CallbackQueryHandler(getlink, pattern='getlink'))
    dispatcher.add_handler(CallbackQueryHandler(onefile, pattern='onefile'))
    dispatcher.add_handler(CallbackQueryHandler(multiplefile, pattern='multiplefile'))
    dispatcher.add_handler(CallbackQueryHandler(delete, pattern='delete'))
    dispatcher.add_handler(CallbackQueryHandler(setting, pattern='setting'))
    dispatcher.add_handler(CallbackQueryHandler(auto_delete, pattern='auto_delete'))
    dispatcher.add_handler(CallbackQueryHandler(file_protect, pattern='file_protect'))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
