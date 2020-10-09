import discord
from discord.ext import commands
import numpy as np
import matplotlib.pyplot as plt
import logging
import os
import pickle


# Logging basic configurations
LEVEL = logging.DEBUG
FORMAT = "%(asctime)s::%(levelname)s::%(message)s"
logging.basicConfig(format=FORMAT, level=LEVEL)

# Disable info and debug logging from discord
logging.getLogger("discord").setLevel(logging.WARNING)

# Pyplot configs
plt.ylim(0, 1)


# Wei Soon client
bot = commands.Bot(command_prefix="ws ")
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
		await ctx.send("```\nUsage: ws hiss <length|NONE>\n```")
	else:
		# Send debug message
		await ctx.send("```\nDebug:\n{}\n```".format(error))


# Py command
@bot.command()
async def py(ctx, *args):
	cmd = " ".join(args)

	try:
		# Try to eval command
		output = eval(cmd)
	except Exception as e:
		# Catch any exceptions and report
		output = e
	finally:
		# Send output of eval
		await ctx.send("```\n{}\n```".format(output))

# Py command error
@py.error
async def py_error(ctx, error):
	# Send debug message
	await ctx.send("```\nDebug:\n{}\n```".format(error))


# Big command
@bot.command()
async def big(ctx, flips: int=1000):
	# Get all die roll sims
	total_sims = flips
	sims = np.array([np.random.binomial(i, 0.5)/i for i in range(1, total_sims)])

	# Plot simulations and save
	plt.plot(np.arange(1, total_sims), sims, "-", scaley=False)
	plt.xlabel("Flips")
	plt.ylabel("Heads %")
	plt.savefig("graph.png")

	# Attach graph as image and send
	graph = discord.File("graph.png")
	sim_graph = discord.Embed(title="Law of Large Numbers")

	await ctx.send(embed=sim_graph, file=graph)

	# Remove and clear graph
	os.remove("graph.png")
	plt.clf()

# Big command error
@big.error
async def big_error(ctx, error):
	if isinstance(error, commands.UserInputError):
		# Send correct usage of command
		await ctx.send("```\nUsage: ws big <flips|NONE>\n```")
	else:
		# Send debug message
		await ctx.send("```\nDebug:\n{}\n```".format(error))


# Help
@bot.command()
async def help(ctx):
	author = ctx.message.author

	# Help command embed content
	notif_msg = discord.Embed(title="I got you my guy")
	help_msg = discord.Embed(title="Help")

	help_msg.add_field(name="misc", value="hiss")
	help_msg.add_field(name="programming", value="py")
	help_msg.add_field(name="ml", value="big")
	help_msg.set_footer(text="Got that punk?")

	# Send help messages
	await author.send(embed=help_msg)
	await ctx.send(embed=notif_msg)


bot.run(os.environ["DISCORD_BOT_KEY"])

