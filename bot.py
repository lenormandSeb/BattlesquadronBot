import os
import discord
from discord.ext.commands import Bot

TOKEN = "NjkwNTg5MTg3Mjk2MTk4NzY2.XnTzqg.B1u6FfRA53WIZqQo5R1cJw9tB8Q"

bot = Bot(command_prefix="!")

@bot.command()
async def testBotMoi(ctx):
    message = await ctx.send(content='coucou {0}'.format(ctx.author.name))

bot.run(TOKEN)
