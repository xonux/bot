import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

SOURCE_CHANNEL_ID = 1499535907626287274
DEST_CHANNEL_ID = 1500502121567490088

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"BOT ONLINE — connecté en tant que {bot.user}")
    print(bot.guilds)
    for guild in bot.guilds:
        print(f"\nServeur : {guild.name}")
        for channel in guild.channels:
            print(f"  #{channel.name} — ID: {channel.id}")
    # Définir le statut en ligne + une activité
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="working if online"
        )
    )

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == SOURCE_CHANNEL_ID:
        try:
            dest_channel = await bot.fetch_channel(DEST_CHANNEL_ID)  # ← API directe
        except discord.NotFound:
            print(f"[ERREUR] Canal introuvable : {DEST_CHANNEL_ID}")
            return
        except discord.Forbidden:
            print("[ERREUR] Pas accès au canal destination.")
            return

        content = f"**{message.author}** :\n{message.content}" if message.content else f"**{message.author}** :"
        files = [await a.to_file() for a in message.attachments]

        try:
            await dest_channel.send(content=content, files=files)
            await message.delete()
        except discord.Forbidden:
            print("[ERREUR] Permissions manquantes pour envoyer ou supprimer.")
        except discord.HTTPException as e:
            print(f"[ERREUR] Échec HTTP : {e}")

    await bot.process_commands(message)

bot.run(os.getenv("TOKEN"))
#python bot.py
