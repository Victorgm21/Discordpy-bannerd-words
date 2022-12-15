import json, os
from discord.ext import commands
import discord
from discord.ext.commands import has_any_role, has_permissions

	
def main():

	def create_config_archive():
		template = {
		'prefix': '!', 
		'token': "introduce tu token", 
		}
		with open('config.json', 'w') as f:
			json.dump(template, f)


	def read_config_archive():
		with open('config.json') as f:
			config_data = json.load(f)
		return config_data


	if not os.path.exists('config.json'):
		print('Creando archivo de configuración')
		create_config_archive()


	# Parametros iniciales
	config_data = read_config_archive()
	prefix = config_data["prefix"]
	token = config_data["token"]
	intents = discord.Intents.all()
	bot = commands.Bot(
		command_prefix = prefix, 
		intents = intents, 
		description = "Bot moderador")


	# Comandos
	# Eventos

	bot.run(token)


if __name__ == '__main__':
	main()