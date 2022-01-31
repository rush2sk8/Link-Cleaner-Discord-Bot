import json
import os
import urllib.parse
from pathlib import Path
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv
from urlextract import URLExtract

load_dotenv(dotenv_path=Path('.')/'.env')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='')

with open("./rules.json", 'r') as rules_file:
    rules = json.loads(rules_file.read())

def clean_url(url):
    print(f'Before: {url}')
    providers = rules["providers"]
    cleaned = url

    for _, provider in providers.items():
        url_pattern = provider["urlPattern"]

        match = re.match(url_pattern, url)

        # if the url matches the glob rule
        if bool(match):

            # regex rule
            for rule in provider["rules"]:
                # remove things that match the rule
                cleaned = re.sub(rule, '', cleaned)

    # remove remaining stuff
    cleaned = re.sub("\?.*","", cleaned)
    cleaned = re.sub('#.*',"", cleaned)
    return cleaned

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
        await message.channel.send(embed=embed)
        await message.delete()

bot.run(DISCORD_TOKEN)
