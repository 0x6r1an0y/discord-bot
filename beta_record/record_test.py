# 此項目依賴pycord
# 務必執行"pip install py-cord"

import discord
import os
from struct import pack, unpack
from discord.ext import tasks
import asyncio
#------------------------------------speech to text
import whisper
model = whisper.load_model("base") #tiny, base, small, medium, large
#------------------------------------speech to text


bot = discord.Bot()
intents = discord.Intents.all()
connections = {}

async def record_obj_producer(ctx):
    voice = ctx.author.voice
    if not voice:
        await ctx.respond("recording...") #已加入聊天室
    record_exec.start(ctx)
    #if ctx.guild.voice_client in bot.voice_clients: #如果已連接 那就單純update cache就好了

async def after_record(vc: discord.VoiceClient):
    await asyncio.sleep(20)
    vc.stop_recording()
    await speech_to_text("record_save")
    
@tasks.loop(seconds=20)
async def record_exec(ctx):
    try:
        voice = ctx.author.voice
        vc: discord.VoiceClient = await voice.channel.connect() 
        connections.update({ctx.guild.id: vc})  # Updating the cache with the guild and channel.
    except Exception:
        vc: discord.VoiceClient = connections[ctx.guild.id]
        
    vc.start_recording(
        discord.sinks.WaveSink(),  # The sink type to use.
        once_done,  # What to do once done.
        ctx.channel #多加一個parameter可以讓機器人在停止錄音的時候離開  # The channel to disconnect from.
    )
    await after_record(vc)
    #await stop_record_exec(ctx)
    # clear all
    
async def speech_to_text(folder_path):
    for file in os.listdir(folder_path):# 先不加, language = 'zh'會有【按下按鈕】的問題
        result = model.transcribe("./" + folder_path + "/" + file) #注意資料夾裡面不要有其他東西或是資料夾
        user_name = await bot.fetch_user(int(file[0:-4])) #檔名就是id
        print((file[0:-4]))
        #print(result["text"])
        if result["text"] != "": #有講話才傳出東西
            print("有講話")
            
            await bot.get_channel(1134498022517116968).send(str(user_name) + " : " + str(result["text"]))
            # 傳送result["text"]到學術探討研究群的語音頻道log
        else:
            print("沒講話")
        os.remove("./" + folder_path + "/" + file)

    
async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args):  # Our voice client already passes these in.
    #recorded_users = [  # A list of recorded users
    #    f"<@{user_id}>"
    #    for user_id, audio in sink.audio_data.items()
    #]
    #await sink.vc.disconnect()  # Disconnect from the voice channel.
    #files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]  # List down the files.
    #-----------------------------------------------
    #'''
    for user_id, audio in sink.audio_data.items():
        filename = "record_save/" + str(user_id) + ".wav"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb+") as f:
            f.write(audio.file.getbuffer())
            
        with open(filename, 'rb+') as f:
            wav_header = "4si4s4sihhiihh4si"
            data = list(unpack(wav_header,f.read(44))) #assign the data format as "4s i 4s 4s i h h i i h h 4s i"
            f.seek(0,2) #start the offset from the end of file
            filesize = f.tell() #the size of the file
            datasize = filesize - 44
            data[-1] = datasize
            data[1]  = datasize+36
            f.seek(0) #start the offset from the start of file
            f.write(pack(wav_header, *data)) #repack the wav file
    #'''
    #-----------------------------------------------
    #await channel.send(f"finished recording audio for: {', '.join(recorded_users)}.", files=files)  # Send a message with the accumulated files.
    #await channel.send("123", files=files)  # Send a message with the accumulated files.

async def stop_record_exec(ctx):  
    if ctx.guild.id in connections:  # Check if the guild is in the cache.
        vc = connections[ctx.guild.id]
        vc.stop_recording()  # Stop recording, and call the callback (once_done).
        del connections[ctx.guild.id]  # Remove the guild from the cache.
        await ctx.delete()  # And delete.
    else:
        await ctx.respond("nnnfd")  # Respond with this if we aren't recording.
        
@bot.command() #實際作用的指令: 開始錄音
async def record(ctx): 
    await record_obj_producer(ctx)
    
@bot.command() #實際作用的指令: 停止錄音
async def stop_record(ctx): 
    record_exec.stop()
    
@bot.event
async def on_ready():
    print(">>>>>>>>>已上線<<<<<<<<<")
    print('目前登入身份：' + os.getlogin() + ":" + str(bot.user))
    #user_name = await bot.fetch_user(310774525446848514) #檔名就是id
    #print(type(str(user_name))) 

bot.run("[SECRET_TOKEN]")
