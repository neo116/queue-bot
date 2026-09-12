import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")


async def load_extensions():
	await bot.load_extension("cogs.queue")


async def main():
	async with bot:
		await load_extensions()
		await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
	import asyncio

	asyncio.run(main())
