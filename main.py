import os
import asyncio

from dotenv import load_dotenv
from pyboy import PyBoy, WindowEvent
import pyboy
import discord
from discord import app_commands


## Load dotenv for token
load_dotenv()
TOKEN = os.getenv('TOKEN')
ROM_PATH = os.getenv('ROM_PATH')
PNG_PATH = 'ss.png'


# Discord client with privileged intent
class Aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        print("Readying")
        if not self.synced:
            await tree.sync(guild=discord.Object(id=809453853879304192))
            self.synced = True
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")


## Emulator buttons
UP_BUTTON = None
DOWN_BUTTON = None
LEFT_BUTTON = None
RIGHT_BUTTON = None
A_BUTTON = None
B_BUTTON = None
START_BUTTON = None
SELECT_BUTTON = None
BUTTONS = [UP_BUTTON, DOWN_BUTTON, LEFT_BUTTON, RIGHT_BUTTON, A_BUTTON, B_BUTTON, START_BUTTON, SELECT_BUTTON]


## Create bot
bot = Aclient()
tree = app_commands.CommandTree(bot)

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
@tree.command(name='connect', description='Connects to the emulator', guild=discord.Object(id=809453853879304192))
async def connect(interaction: discord.Interaction):
    await interaction.response.send_message(content="Pokemon")
    while True:
        emu.screen_image().save(PNG_PATH)
        await interaction.edit_original_message(content="Pokemon", 
            attachments=[discord.File(PNG_PATH)]
        )
        await asyncio.sleep(0.5)

@tree.command(name='up', description='Presses the UP button', guild=discord.Object(id=809453853879304192))
async def up(interaction: discord.Interaction):
    emu.send_input(WindowEvent.PRESS_ARROW_UP)
    emu.send_input(WindowEvent.RELEASE_ARROW_UP)
    await interaction.delete_original_message()

@tree.command(name='down', description='Presses the DOWN button', guild=discord.Object(id=809453853879304192))
async def down(interaction: discord.Interaction):
    emu.send_input(WindowEvent.PRESS_ARROW_DOWN)
    emu.send_input(WindowEvent.RELEASE_ARROW_DOWN)
    await interaction.delete_original_message()

@tree.command(name='left', description='Presses the LEFT button', guild=discord.Object(id=809453853879304192))
async def left(interaction: discord.Interaction):
    emu.send_input(WindowEvent.PRESS_ARROW_LEFT)
    emu.send_input(WindowEvent.RELEASE_ARROW_LEFT)
    await interaction.delete_original_message()

@tree.command(name='right', description='Presses the RIGHT button', guild=discord.Object(id=809453853879304192))
async def right(interaction: discord.Interaction):
    emu.send_input(WindowEvent.PRESS_ARROW_RIGHT)
    emu.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
    await interaction.delete_original_message()

@tree.command(name='a', description='Presses the A button', guild=discord.Object(id=809453853879304192))
async def a(interaction: discord.Interaction):
    print("A")
    emu.send_input(WindowEvent.PRESS_BUTTON_A)
    emu.send_input(WindowEvent.RELEASE_BUTTON_A)
    await interaction.delete_original_message()

@tree.command(name='b', description='Presses the B button', guild=discord.Object(id=809453853879304192))
async def b(interaction: discord.Interaction):
    emu.send_input(WindowEvent.PRESS_BUTTON_B)
    emu.send_input(WindowEvent.RELEASE_BUTTON_B)
    await interaction.delete_original_message()


async def main():
    async with bot:
        bot.loop.create_task(tick_emulator())
        await bot.start(TOKEN)

## Start the bot
if __name__ == '__main__':
    asyncio.run(main())
