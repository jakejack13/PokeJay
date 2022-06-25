# import logging
import os
import asyncio
# import logging
from tempfile import TemporaryFile

from dotenv import load_dotenv
import interactions
from pyboy import PyBoy
import discord

## Load dotenv for token
load_dotenv()
TOKEN = os.getenv('TOKEN')
ROM_PATH = os.getenv('ROM_PATH')

## Set up logging 
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)


## Emulator buttons
UP_BUTTON = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Up",
    custom_id="UP_BUTTON"
)
DOWN_BUTTON = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Down",
    custom_id="DOWN_BUTTON"
)
LEFT_BUTTON = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Left",
    custom_id="LEFT_BUTTON"
)
RIGHT_BUTTON = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Right",
    custom_id="RIGHT_BUTTON"
)
A_BUTTON = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="A",
    custom_id="A_BUTTON"
)
B_BUTTON = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="B",
    custom_id="B_BUTTON"
)
START_BUTTON = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Start",
    custom_id="START_BUTTON"
)
SELECT_BUTTON = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Select",
    custom_id="SELECT_BUTTON"
)
BUTTONS = [UP_BUTTON, DOWN_BUTTON, LEFT_BUTTON, RIGHT_BUTTON, A_BUTTON, B_BUTTON, START_BUTTON, SELECT_BUTTON]

## Create temporary file for image processing
temp_img = TemporaryFile()

## Create bot
bot = interactions.Client(token=TOKEN)

## Start emulator
emu = PyBoy(ROM_PATH)

## Async emulator infinite loop
async def tick_emulator():
    await bot.wait_until_ready()
    try:
        with open(ROM_PATH + '.state') as f:
            emu.load_state(f)
    except:
        pass
    while not emu.tick():
        pass
    emu.save_state()


## Commands
@bot.command(name='connect', description='Connect to the emulator')
async def connect(ctx: interactions.CommandContext):
    # while True:
    emu.screen_image().save(temp_img,format='png')
    await ctx.send(interactions.File(fp=temp_img), components=BUTTONS)
    # await ctx.get_channel().send(files=interactions.File(fp=temp_img), components=BUTTONS)
    # await asyncio.sleep(0.5)


## Set up event loops for emulator running alongside bot
loop = asyncio.get_event_loop()
task2 = loop.create_task(tick_emulator())
task1 = loop.create_task(bot._ready())
gathered = asyncio.gather(task1, task2)


## Start the bot
if __name__ == '__main__':
    loop.run_until_complete(gathered)
