import os
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv
from urlextract import URLExtract
import unalix

load_dotenv(dotenv_path=Path('.')/'.env')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='')


def clean_url(url):
    return unalix.clear_url(url)

@bot.event
async def on_ready():
    """Event when the bot logs in"""
    await bot.change_presence(activity=discord.Streaming(name="by rush2sk8", url='https://www.twitch.tv/rush2sk8'))
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    m = message.content
    extractor = URLExtract()
    found = extractor.find_urls(m)

    if len(found) > 0:
        for url in found:
            cleaned = clean_url(url)
            m = m.replace(url, cleaned)

        if message.content == m:
            return

        embed=discord.Embed(title="Trackers Cleaned", description=m)
        embed.set_author(name=f'@{message.author.name}')

        print(f'before: {message.content}')
        print(f'after: {cleaned}')
        await message.channel.send(embed=embed)
        await message.delete()

bot.run(DISCORD_TOKEN)
