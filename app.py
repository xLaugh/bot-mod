import discord
from discord.ext import tasks
import re

CHANNEL_ID = 702861467577352203
ALLOWED_DOMAINS = [
    'laugh.yt',
    'x.com/thatxlaugh',
    'twitter.com/thatxlaugh'
]

BANNED_CONTENT = {
    '卐', '卍', '⚡⚡', '88', '1488', 
    'connard', 'pute', 'salope', 'enculé', 'fdp', 'ntm', 'tg', 'ta gueule',
    'fuck', 'bitch', 'whore', 'cunt', 'retard', 'faggot', 'nigger', 'nigga',
    'puta', 'mierda', 'pendejo', 'maricon', 'hijo de puta',
    'scheiße', 'hurensohn', 'fotze', 'arschloch',
    'stronzo', 'cazzo', 'puttana', 'vaffanculo',
}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} est connecté!')
    check_messages.start()

@tasks.loop(seconds=30)
async def check_messages():
    try:
        channel = client.get_channel(CHANNEL_ID)
        if not channel:
            return

        async for message in channel.history(limit=100):
            if message.author == client.user:
                continue

            should_delete = False
            message_lower = message.content.lower()
            contains_banned_content = any(word in message_lower for word in BANNED_CONTENT)

            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
            
            if urls:
                for url in urls:
                    is_allowed = False
                    for allowed_domain in ALLOWED_DOMAINS:
                        if allowed_domain in url:
                            is_allowed = True
                            break
                    if not is_allowed:
                        should_delete = True
                        break

            if should_delete or contains_banned_content:
                try:
                    await message.delete()
                    print(f"Message supprimé: {message.content}")
                except discord.errors.NotFound:
                    pass
                except discord.errors.Forbidden:
                    print("Permissions insuffisantes pour supprimer le message")

    except Exception as e:
        print(f"Erreur: {e}")

client.run('TOKEN')
