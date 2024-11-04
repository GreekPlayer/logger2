import discord
from discord.ext import commands

# Replace 'YOUR_BOT_TOKEN' with your bot's token
TOKEN = 'YOUR_BOT_TOKEN'
# Replace 'YOUR_CHANNEL_ID' with the channel ID where you want to log messages
LOG_CHANNEL_ID = 123456789012345678  # Example: replace with actual channel ID

intents = discord.Intents.default()
intents.members = True               # Required for member join/leave events
intents.message_content = True        # Required for logging messages
intents.guilds = True
intents.bans = True                   # Required for ban/unban events
intents.guild_messages = True         # Required for message events
intents.voice_states = True           # Required for voice activity

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('------')

@bot.event
async def on_member_join(member):
    # Log join message in a specific channel
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f'🚪 **Join:** {member.mention} has joined the server.')

@bot.event
async def on_member_remove(member):
    # Log leave message in a specific channel
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f'🚶 **Leave:** {member.mention} has left the server.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Log message in a specific channel
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f'💬 **Message:** {message.author} in {message.channel}: {message.content}')

@bot.event
async def on_message_delete(message):
    # Log message deletion
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f'🗑️ **Deleted Message:** {message.author} in {message.channel}: {message.content}')

@bot.event
async def on_message_edit(before, after):
    # Log message edits
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(
            f'✏️ **Edited Message:** {before.author} in {before.channel}\n'
            f'**Before:** {before.content}\n'
            f'**After:** {after.content}'
        )

@bot.event
async def on_voice_state_update(member, before, after):
    # Log voice channel join/leave/move
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if not channel:
        return
    
    if before.channel is None and after.channel is not None:
        await channel.send(f'🔊 **Voice Join:** {member.mention} joined {after.channel.name}')
    elif before.channel is not None and after.channel is None:
        await channel.send(f'🔇 **Voice Leave:** {member.mention} left {before.channel.name}')
    elif before.channel != after.channel:
        await channel.send(f'🔄 **Voice Move:** {member.mention} moved from {before.channel.name} to {after.channel.name}')

@bot.event
async def on_member_ban(guild, user):
    # Log ban events
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f'⛔ **Ban:** {user.mention} has been banned from the server.')

@bot.event
async def on_member_unban(guild, user):
    # Log unban events
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f'✅ **Unban:** {user.mention} has been unbanned.')

@bot.event
async def on_member_remove(member):
    # Log kick event - usually inferred from a leave if permissions allow
    # (Discord doesn't have a direct on_member_kick event)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f'👢 **Kick (or Leave):** {member.mention} has left the server.')

bot.run(TOKEN)
