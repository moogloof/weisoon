import tasks
import discord
from discord.ext import commands
import logging
import os
import pickle


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


# Tasks command
@bot.command()
async def task(ctx, action, *args):
	msg_str = "```\n"

	# List tasks
	if action == "list":
		# Task list string
		msg_str += "Tasks:\n\n"

		# List all tasknames
		for taskname in os.listdir("tasks"):
			# Get task path
			taskpath = os.path.join("tasks", taskname)

			with open(taskpath, "rb") as f:
				# Load task
				task = pickle.load(f)

				# Add task to list
				msg_str += "	{} :: {}\n".format(task.name, task.status)

	# Add task
	if action == "add":
		# Create task
		task = tasks.Task(args[0])

		if len(args) > 1:
			task.description = args[1]

		task.save()

		msg_str += "Successfully created task.\n"

	# View task detail
	if action == "view":
		# Get task
		task = tasks.Task.load(args[0])

		# Display task info
		msg_str += "Task name: {}\n".format(task.name)
		msg_str += "Task description: {}\n".format(task.description)
		msg_str += "Task status: {}\n".format(task.status)

	# Send message string
	msg_str += "```"
	await ctx.send(msg_str)

# Task command error
@task.error
async def task_error(ctx, error):
	if isinstance(error, commands.UserInputError):
		# Send correct usages
		await ctx.send("""
```
Usages:

m#task list
m#task add <title> <description|NONE>
m#task view <title>
```
""")
	else:
		await ctx.send("```\nError: {}\n```".format(error))


# Help command
@bot.command()
async def help(ctx):
	author = ctx.message.author

	# Help command embed content
	help_msg = """
```
Help:

  Miscellaneous -

    m#hiss - Hisses


  Projects -

    m#tasks - Manage tasks
```
"""

	# Send help messages
	await author.send(help_msg)
	await ctx.send("```\nYo I got you dog\n```")


bot.run(os.environ["DISCORD_BOT_KEY"])

