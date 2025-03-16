import sys
import glob
import importlib
from pathlib import Path
import logging
import logging.config
import asyncio
from pyrogram import Client, idle
from pyrogram import types
from datetime import date, datetime
import pytz
from aiohttp import web
from TechVJ.server import web_server
from TechVJ.bot import StreamBot
from TechVJ.utils.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients
from plugins.clone import restart_bots
from config import LOG_CHANNEL, ON_HEROKU, CLONE_MODE, PORT
from Script import script

# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Configure logging
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

# Path to plugins directory
ppath = "plugins/*.py"
files = glob.glob(ppath)

# Start the StreamBot
StreamBot.start()

# Create event loop
loop = asyncio.get_event_loop()

# Main asynchronous function to start the bot
async def start():
    print('\n')
    print('Initializing Tech VJ Bot')

    # Fetch bot information
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username

    # Initialize clients (if any)
    await initialize_clients()

    # Load all plugins
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print(f"Tech VJ Imported => {plugin_name}")

    # If deployed on Heroku, ping server for keep-alive
    if ON_HEROKU:
        asyncio.create_task(ping_server())

    # Send restart message to the log channel
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    await StreamBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))

    # Start the web server for bot keep-alive
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()

    # If in clone mode, restart other bots
    if CLONE_MODE:
        await restart_bots()

    print("Bot Started Powered By @VJ_Botz")

    # Idle the bot and keep it running
    await idle()

# Main entry point to run the bot
if __name__ == '__main__':
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
