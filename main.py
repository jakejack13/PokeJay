import os
import asyncio

from dotenv import load_dotenv
from pyboy import PyBoy, WindowEvent
import discord


## Load dotenv for token
load_dotenv()
TOKEN = os.getenv('TOKEN')
ROM_PATH = os.getenv('ROM_PATH')
PNG_PATH = 'ss.png'


## Create bot
bot = discord.Client(intents=discord.Intents.all())

## Start emulator
emu = PyBoy(ROM_PATH)

## Async emulator infinite loop
async def tick_emulator():
    await bot.wait_until_ready()
    # try:
    #     with open(ROM_PATH + '.state') as f:
    #         emu.load_state(f)
    # except:
    #     pass
    while not emu.tick():
        await asyncio.sleep(0.05)
    # emu.save_state()


## Commands
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # if message.content == 'test':
    #     await message.channel.send('hello')

    if message.content.startswith('!connect'):
        screen_message = await message.channel.send('Pokemon')
        while True:
            emu.screen_image().save(PNG_PATH)
            await screen_message.edit(content='', attachments=[discord.File(PNG_PATH)])
            await asyncio.sleep(1)
        
    elif message.content == 'up':
        emu.send_input(WindowEvent.PRESS_ARROW_UP)
        emu.tick()
        emu.send_input(WindowEvent.RELEASE_ARROW_UP)
        await message.delete()
    elif message.content == 'down':
        emu.send_input(WindowEvent.PRESS_ARROW_DOWN)
        emu.tick()
        emu.send_input(WindowEvent.RELEASE_ARROW_DOWN)
        await message.delete()
    elif message.content == 'left':
        emu.send_input(WindowEvent.PRESS_ARROW_LEFT)
        emu.tick()
        emu.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        await message.delete()
    elif message.content == 'right':
        emu.send_input(WindowEvent.PRESS_ARROW_RIGHT)
        emu.tick()
        emu.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        await message.delete()
    elif message.content == 'a':
        emu.send_input(WindowEvent.PRESS_BUTTON_A)
        emu.tick()
        emu.send_input(WindowEvent.RELEASE_BUTTON_A)
        await message.delete()
    elif message.content == 'b':
        emu.send_input(WindowEvent.PRESS_BUTTON_B)
        emu.tick()
        emu.send_input(WindowEvent.RELEASE_BUTTON_B)
        await message.delete()
    elif message.content == 'start':
        emu.send_input(WindowEvent.PRESS_BUTTON_START)
        emu.tick()
        emu.send_input(WindowEvent.RELEASE_BUTTON_START)
        await message.delete()
    elif message.content == 'select':
        emu.send_input(WindowEvent.PRESS_BUTTON_SELECT)
        emu.tick()
        emu.send_input(WindowEvent.RELEASE_BUTTON_SELECT)
        await message.delete()


async def main():
    async with bot:
        bot.loop.create_task(tick_emulator())
        await bot.start(TOKEN)

## Start the bot
if __name__ == '__main__':
    asyncio.run(main())
    # bot.run(TOKEN)
