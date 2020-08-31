import pickle
import os


# Task statuses
ACTIVE = "active"
STALE = "stale"
UNDER_REVIEW = "under review"


# Task class
class Task:
	def __init__(self, title, description=None, status=ACTIVE):
		self.status = status
		self.title = title
		self.description = description

	def save(self):
		# Get filename and path
		filename = "{}.task".format(self.title)
		filepath = os.path.join("tasks", filename)

		# Dump task in file
		with open(filepath, "wb") as f:
			pickle.dump(self, f)

	@staticmethod
	def load(title):
		# Load task from name
		filename = "{}.task".format(title)
		filepath = os.path.join("tasks", filename)

		with open(filepath, "rb") as f:
			return pickle.load(f)

