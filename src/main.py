import discord
from discord.ext import commands
import logging
import os


# Logging basic configurations
LEVEL = logging.DEBUG
FORMAT = "%(asctime)s::%(levelname)s::%(message)s"
logging.basicConfig(format=FORMAT, level=LEVEL)

# Disable info and debug logging from discord
logging.getLogger("discord").setLevel(logging.WARNING)


# Wei Soon client
bot = commands.Bot(command_prefix="m#")
bot.remove_command("help")

# Hiss command
@bot.command()
async def hiss(ctx, length: int=100):
	hiss_str = "hi" + "s"*min(12000, length)

	# Post hiss string in chunks
	while hiss_str:
		await ctx.send("```\n" + hiss_str[:1992] + "\n```")
		hiss_str = hiss_str[1992:]

# Hiss command error
@hiss.error
async def hiss_error(ctx, error):
	if isinstance(error, commands.UserInputError):
		# Send correct usage of command
		await ctx.send("```\nUsage: m!hiss <int|NONE>\n```")


# Help command
@bot.command()
async def help(ctx):
	author = ctx.message.author

	embed = discord.Embed(colour=discord.Colour.orange())

	# Help command embed content
	embed.set_author(name="Help")
	embed.add_field(name="m#hiss", value="Returns hiss", inline=False)

	# Send help messages
	await author.send(embed=embed)
	await ctx.send("```\nYo I got you dog\n```")


bot.run(os.environ["DISCORD_BOT_KEY"])

