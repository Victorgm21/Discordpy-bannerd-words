import json, os
from discord.ext import commands
import discord
from discord.ext.commands import has_permissions


class Crear_Respuesta():
	def __init__(self, content):
		self.title = 'Comando ejecutado:'
		self.content = content

	@property
	def enviar(self):
		self.respuesta = discord.Embed(
			title = self.title,
			description = self.content,
			colour = int("DC75FF", 16)
			)
		return self.respuesta


def main():

	def create_config_archive():
		template = {
		'prefix': '!', 
		'token': "introduce tu token", 
		'palabrasbaneadas': []}
		with open('config.json', 'w') as f:
			json.dump(template, f)


	def read_config_archive():
		with open('config.json') as f:
			config_data = json.load(f)
		return config_data


	if not os.path.exists('config.json'):
		print('Creando archivo de configuración')
		create_config_archive()

	config_data = read_config_archive()
	palabrasbaneadas = config_data["palabrasbaneadas"]
	prefix = config_data["prefix"]
	token = config_data["token"]
	intents = discord.Intents.all()
	bot = commands.Bot(
		command_prefix = prefix, 
		intents = intents, 
		description = "Bot moderador")

	# Comandos

	@bot.command(help='te envia un mensaje al MD')
	async def respondeme(ctx):
		print(ctx.author)
		await ctx.author.send(content='ola amigo como estas :D ')


	@bot.command(help='Lista de roles a los que perteneces.')
	async def rol_list(ctx):
		roles = ''
		for rol in ctx.author.roles:
			roles += rol.name + ', '
		respuesta = Crear_Respuesta(f'Usted pertenece a los siguientes roles: {roles}')
		await ctx.reply(embed = respuesta.enviar)


	@bot.command(help='Cambia el prefijo de los comandos del bot.')
	@has_permissions(administrator=True)
	async def changeprefix(ctx, new_prefix):
		if new_prefix == str(bot.command_prefix):
			respuesta = Crear_Respuesta('Ya estas usando ese prefijo actualmente.')
			await ctx.reply(embed = respuesta.enviar)
		else:
			with open('config.json', 'r+') as f:
				datos = json.load(f)
				datos['prefix'] = new_prefix
				f.seek(0)
				f.write(json.dumps(datos))
				f.truncate()
			bot.command_prefix = new_prefix
			respuesta= Crear_Respuesta('Se ha cambiado el prefijo del bot.')
			await ctx.reply(embed = respuesta.enviar)


	@bot.command(help='Banear palabra del servidor')
	@has_permissions(administrator=True)
	async def banword(ctx, palabra):
		if palabra.lower() in palabrasbaneadas:
			respuesta = Crear_Respuesta('Esa palabra ha sido baneada anteriormente.')
			await ctx.send(embed = respuesta.enviar)
		else:
			palabrasbaneadas.append(palabra.lower())
			with open('config.json', 'r+') as f:
				datos = json.load(f)
				datos['palabrasbaneadas'] = palabrasbaneadas
				f.seek(0)
				f.write(json.dumps(datos))
				f.truncate()
			respuesta = Crear_Respuesta('Palabra baneada correctamente del SV')
			await ctx.send(embed = respuesta.enviar)


	@bot.command(help = 'Quitar ban a palabra del servidor')
	@has_permissions(administrator=True)
	async def unbanword(ctx, palabra):
		if palabra.lower() in palabrasbaneadas:
			palabrasbaneadas.remove(palabra.lower())
			with open('config.json', 'r+') as f:
				datos = json.load(f)
				datos['palabrasbaneadas'] = palabrasbaneadas
				f.seek(0)
				f.write(json.dumps(datos))
				f.truncate()
			respuesta = Crear_Respuesta('Palabra desbaneada correctamente del servidor.')
			await ctx.send(embed= respuesta.enviar)
		else:
			respuesta = Crear_Respuesta('Esa palabra no esta baneada del servidor.')
			await ctx.send(embed = respuesta.enviar)

	# Eventos
	@bot.event ###
	async def on_message(message):
		message_content = message.content.lower()
		message_content = message_content.split(' ')
		for palabrabaneada in palabrasbaneadas:
			if palabrabaneada in message_content:
				respuesta = Crear_Respuesta('Cuida tú vocabulario, porfavor.')
				respuesta.title='De parte de los moderadores:'
				await message.reply(embed = respuesta.enviar)
				await message.delete()
				break
		await bot.process_commands(message)

	@bot.event #######
	async def on_ready():
	    # activity = discord.Streaming(name="Stream", url='https://www.twitch.tv/elmiillor')
	    activity=discord.Activity(type=discord.ActivityType.listening, name="Conejito malo")
	    await bot.change_presence(activity=activity)
	    #await bot.change_presence(status=discord.Status.dnd, activity=activity)
	    print("Bot is ready!")

	bot.run(token)


if __name__ == '__main__':
	main()