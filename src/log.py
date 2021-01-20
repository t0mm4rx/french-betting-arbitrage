import discord_notify as dn
from datetime import datetime

URL = "https://discord.com/api/webhooks/801389334615949342/E0KM3HN5jvoOapgt6uXdEQ-fmT5A5m8LUZkBYAEH1FmC8UQrbZ2pbjEtdaSBx90HL_Kt"

def init():
	global filename
	filename = "./{}.log".format(datetime.now().strftime("%d.%m.%Y_%H:%M:%S"))
	with open(filename, "w+") as _:
		pass

def log(message, end="\n"):
	with open(filename, 'a') as file:
		file.write(message + end)

def discord(message):
	notifier = dn.Notifier(URL)
	notifier.send(message, print_message=False)