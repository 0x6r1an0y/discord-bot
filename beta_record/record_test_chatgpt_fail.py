import discord
import os
import asyncio
from discord.ext import tasks

# Import whisper model
import whisper

# Load whisper model
model = whisper.load_model("medium")

# Initialize bot
bot = discord.Bot()
intents = discord.Intents.all()
connections = {}

# Variable to track recording status
recording = False

# Function to start recording
async def start_recording(ctx):
    global recording
    voice = ctx.author.voice
    if not voice:
        await ctx.respond("cccc")  # 已加入聊天室
        return

    try:
        vc: discord.VoiceClient = await voice.channel.connect()
        connections[ctx.guild.id] = vc  # 更新 cache
    except Exception:
        vc: discord.VoiceClient = connections[ctx.guild.id]

    if not recording:
        recording = True
        # Start recording loop
        record_loop.start(vc, ctx.channel)
    else:
        await ctx.respond("Recording already in progress.")

# Function to stop recording
async def stop_recording(ctx):
    global recording
    if ctx.guild.id in connections:
        vc = connections[ctx.guild.id]
        record_loop.cancel()  # 停止錄音循環
        await vc.disconnect()
        del connections[ctx.guild.id]
        recording = False
        await ctx.delete()
    else:
        await ctx.respond("Recording not in progress.")

# Function to handle recording loop
@tasks.loop(seconds=20)
async def record_loop(vc, channel):
    vc.start_recording(discord.sinks.WaveSink(), lambda sink: asyncio.ensure_future(after_record(vc, sink, channel)))

# Function to handle recording completion
async def after_record(vc, sink, channel):
    vc.stop_recording()  # 停止錄音
    await transcribe_audio("record_save", channel)

# Function to transcribe audio to text
async def transcribe_audio(folder_path, channel):
    for file in os.listdir(folder_path):
        result = model.transcribe(os.path.join(folder_path, file))
        user_name = await bot.fetch_user(int(file[0:-4]))
        if result["text"] != "":
            await channel.send(str(user_name) + " : " + str(result["text"]))
        os.remove(os.path.join(folder_path, file))

# Command to start recording
@bot.command()
async def record(ctx):
    await start_recording(ctx)

# Command to stop recording
@bot.command()
async def stop_record(ctx):
    await stop_recording(ctx)

# Event when bot is ready
@bot.event
async def on_ready():
    print(">>>>>>>>> 已上線 <<<<<<<<<")
    print('目前登入身份：' + os.getlogin() + ":" + str(bot.user))

# Run bot
bot.run("[SECRET_TOKEN]")
