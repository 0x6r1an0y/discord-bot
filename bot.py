#auto py to exe ->Manual Argument Input-> --collect-data grapheme
#only python >3.9 <=3.11

#TODO: 要把chrome chromedriver做在裡面
#TODO: 分離式python 與全域分開
#TODO: 天罰計數器做在init裡面
#TODO: BOT object化
#TODO: database.write

from mod.autochromedriver import upgrade_chromedriver
#from auto_roll_call.roll_call_self_test import roll_call_test
import discord
from discord.ext import commands,tasks
import random
import os
import time
import nacl
from alive_progress import alive_bar
import datetime #給bot.py編輯時間用
import psutil #給取得記憶體用量用
from pathlib import Path
from mod.environment_variables import init 
from mod.addlog import serverlog, botlog#不要用print()，而是用botlog().debug()或severlog.info()等等
from mod.emoji_role import * #import know_emoji_find_id,know_emoji_find_name,know_id_find_emoji,know_id_find_name,know_name_find_emoji,know_name_find_id#我就一次引入全部了
from mod.message_process import message_process
from mod.voice_chat_log import voice_chat_log
from mod.message_manager import MessageManager
#from mod.japan_ticket import japan
import sys
import platform

PYTHON_VER:str = platform.python_version()

#ctx: commands.context.Context
#不可以ctx: discord.ext.commands.context.Context
#ctx是discord目錄下的一個資料夾 沒有寫在init裡面
VERSION = "4.2"
ID,TOKEN,SERVERWEBHOOK,BOTWEBHOOK,MORNING = init()
counter_for_MOTD = 0
STATUS_MSG_ID = 1412141519577550921 # 狀態訊息相關變數

status_channel: MessageManager = None
bot_start_time = datetime.datetime.now()

message_manager = None # 建立訊息管理器實例 (在bot初始化後建立)

 #--------------------------------------------------------------------------------------------
 
async def penalty_button_kick(interaction: discord.interactions.Interaction)-> None:
    # 如果不interaction.response 會顯示此交互失敗
    # ephemeral parameter就是傳送只有當事人看的到的訊息

    user_obj: discord.member.Member = interaction.user
    user_id: int = user_obj.id
    # 不能透過bot.guild來fetch guild 會有問題
    guild_object: discord.Guild = interaction.guild
    user_object: discord.Member = await guild_object.fetch_member(user_id) #aka perpetrator
    if user_object.voice == None:
        await interaction.response.send_message('🤌你要先加入一個這邊的語音頻道才可以玩天罰喔🤌', ephemeral=True) 
        return None
    # 如果使用者沒有加入頻道就會直接return none
    
    user_voice_channel_object: discord.VoiceChannel = user_object.voice.channel 
    users_in_voice_channel_object: list[discord.Member] = user_voice_channel_object.members
    num_users_in_voice_channel: int = len(users_in_voice_channel_object)
    if (num_users_in_voice_channel == 1):
        await interaction.response.send_message('🤔 你想把你自己踢掉喔? 🤔', ephemeral=True)
        return None
    # 如果只有一個人就會直接return none
    picked_user_index: int = random.randint(0,num_users_in_voice_channel-1) # index所以-1
    perpetrator_user_object: discord.Member = user_object
    victim_user_object: discord.Member = users_in_voice_channel_object[picked_user_index]
    msg: str = '👎❌ 你超壞 😈😔\n把 '+ str(victim_user_object) +'踢出去了'
    if victim_user_object == perpetrator_user_object:
        msg: str = 'ㄨㄚˊ 人在做天在看👀 記得扶老太太過馬路才不會把自己踢出去 '
    try: 
        await victim_user_object.move_to(None) # move to none 就是踢出去
        await interaction.response.send_message(msg, ephemeral=True)
        serverlog().info(str(perpetrator_user_object) + " 把 " + str(victim_user_object) +'踢出去了')
    except Exception as e:
        serverlog().error("在天罰時遇到了以下問題，通常是此機器人在該伺服器的權限不足導致的\n" + str(e))
    
class penalty_button(discord.ui.View):
    #ToDO: 每一個人的天罰 冷卻時間
    #ref: https://github.com/Rapptz/discord.py/blob/master/examples/views/persistent.py
    
    def __init__(self):
        super().__init__(timeout=None) #讓按鈕不會有3分鐘冷卻無法再按的限制
        
    @discord.ui.button(label="死亡計數器: 0", style=discord.ButtonStyle.green, custom_id='penalty')#custom_id 必須為每一個按鈕設定獨一無二的id (lengh<100)
    async def counter(self, button: discord.ui.Button, interaction: discord.Interaction):
        number = int(button.label[7:])
        button.label = '死亡計數器: ' + str(number + 1)
        await penalty_button_kick(interaction)
        await interaction.message.edit(view=self)
        

 #--------------------------------------------------------------------------------------------
    
class Lijiu_bot(commands.Bot): #繼承bot
    def __init__(self) -> None:
        intents = discord.Intents.all()
        intents.message_content = True #v2
        intents.members = True
        super().__init__(command_prefix=commands.when_mentioned_or(','), intents=intents)
        
 #--------------------------------------------------------------------------------------------
bot = Lijiu_bot()
 #--------------------------------------------------------------------------------------------

@bot.event
async def on_ready():
    global status_channel, bot_start_time, message_manager
    botlog().info(">>>>>>>>>已上線<<<<<<<<<")
    botlog().info('目前登入身份：' + os.getlogin() + ":" + str(bot.user))
    bot.add_view(penalty_button()) #讓機器人重新開機後還有辦法使用天罰
    
    # 初始化訊息管理器
    message_manager = MessageManager(bot)
    botlog().info("訊息管理器已初始化")

    if not presence_loop.is_running():# 以防出現RuntimeError: Task is already launched and is not completed.的狀況
        presence_loop.start() 
    if not check_loop.is_running():
        check_loop.start()
    if not status_update_loop.is_running():
        status_update_loop.start() #這邊需要refactor
    # await roll_call_test()
    
    
@tasks.loop(seconds=3)
async def presence_loop():
    #start = time.time()
    total_members = []
    global counter_for_MOTD
    for guild in bot.guilds:
        total_members.extend(guild.members)
    total_members_count = len(set(total_members))
    presence = [
        "ohohoh",
        str(total_members_count) + "個二逼卵子在看我",
        "hihihi"
    ]
    # reset counter_for_MOTD
    if (counter_for_MOTD >= len(presence)):
        counter_for_MOTD = 0

    game = discord.Game(presence[counter_for_MOTD])
    counter_for_MOTD += 1
    #end = time.time()
    #botlog().info(end - start)
    await bot.change_presence(status=discord.Status.online, activity=game)

@tasks.loop(hours=1)
async def check_loop():
    serverlog().info("heartbeat")

@tasks.loop(seconds=30)
async def status_update_loop():
    global STATUS_MSG_ID, status_channel
    if STATUS_MSG_ID is None or status_channel is None:
        return
    
    try:
        # 獲取最後上線時間
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 這是開機器人的時間
        last_online_time = bot_start_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 獲取版本
        version = VERSION
        
        # 獲取bot.py的最後修改時間
        bot_file_path = Path(__file__)
        last_modified = datetime.datetime.fromtimestamp(bot_file_path.stat().st_mtime)
        last_update_time = last_modified.strftime("%Y-%m-%d %H:%M:%S")
        
        # 獲取記憶體使用量
        process = psutil.Process()
        memory_usage = f"{process.memory_info().rss / 1024 / 1024:.2f} MB"
        
        # 獲取延遲
        # bug fixing: cannot convert float infinity to integer
        if bot.latency == float('inf'):
            latency = f"暫時無法取得"
        else:
            latency = f"{round(bot.latency*1000)} ms"
        # latency = f"{round(bot.latency*1000)} ms"
        
        # 獲取伺服器和使用者數量
        total_guilds = len(bot.guilds)
        total_members = []
        for guild in bot.guilds:
            total_members.extend(guild.members)
        total_members_count = len(set(total_members))
        users_info = f"伺服器: {total_guilds} | 使用者: {total_members_count}"

        # 更新embed
        embed = discord.Embed(title="小梨酒機器人", description="最新上線時間狀態檢查", color=0x8b3c3c)
        embed.add_field(name="腳本更新時間", value=last_update_time, inline=True)
        embed.add_field(name="服務啟動時間", value=last_online_time, inline=True)
        embed.add_field(name="機器人最新上線時間", value=now_time, inline=True)
        embed.add_field(name="版本", value=version, inline=True)
        embed.add_field(name="記憶體", value=memory_usage, inline=True)
        
        # 獲取 CPU 資訊
        try:
            from mod.platform_config import config
            cpu_usage = config.get_cpu_usage()
            cpu_temp = config.get_cpu_temperature()
        except ImportError:
            cpu_usage = "模組載入失敗"
            cpu_temp = "模組載入失敗"
        except Exception as e:
            cpu_usage = f"取得失敗: {str(e)}"
            cpu_temp = f"取得失敗: {str(e)}"
        
        embed.add_field(name="cpu占用率", value=cpu_usage, inline=True)
        embed.add_field(name="cpu溫度", value=cpu_temp, inline=True)
        embed.add_field(name="延遲", value=latency, inline=True)
        embed.add_field(name="二逼卵子數", value=users_info, inline=True)
        embed.add_field(name="Python版本", value=PYTHON_VER, inline=True)
        
        # 使用平台配置獲取更詳細的資訊
        try:
            from mod.platform_config import config
            platform_info = config.get_platform_info()
            platform_text = f"{platform_info['node']}@{platform_info['system']} {platform_info['machine']}"
        except ImportError:
            platform_text = f"{platform.node()}@{platform.platform()}"
        
        embed.add_field(name="運作者", value=platform_text, inline=True)

        # 更新訊息 - 使用MessageManager
        if message_manager:
            success = await message_manager.update_message(STATUS_MSG_ID, embed)
        
    except Exception as e:
        serverlog().error(f"狀態更新失敗: {e}")


@bot.event
async def on_member_join(member):
    serverlog().info(f'{member} 加入了伺服器!') #=print(member + "join!")
    # channel = bot.get_channel(int(ID))
    # await channel.send(f'{member} 一支一支棒棒')

@bot.event
async def on_member_remove(member):
    serverlog().info(f'{member} 離開了伺服器!')
    # channel = bot.get_channel(int(ID))
    # await channel.send(f'{member} 真假:(')

@bot.command()
async def ping(ctx: commands.context.Context):
    await ctx.send(f'{round(bot.latency*1000)} ms') 

'''
@bot.command()
async def morning(ctx: commands.context.Context):
    random_pic = random.choice(MORNING)
    pic = discord.File(random_pic)
    botlog().debug(f'Good morning 指令已偵測 {ctx},')
    botlog().debug(f'送出{random_pic} !')
    await ctx.send(file = pic)
'''

@bot.command()
async def skip(ctx: commands.context.Context):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

@bot.command()
async def create_penalty_button(ctx: commands.context.Context):
    await ctx.send(view=penalty_button())

@bot.command()
async def create_select_identity(ctx: commands.context.Context):
    embed=discord.Embed(title="身分組", description="自己選擇需要的身分組，如果無法運作就找離九八八踹共", color=0xbdf7ff)
    embed.set_image(url="https://obs.line-scdn.net/0hzmZ4fmppJUJnTTKByc5aFV8bKTNUKz9LRSlqdBFPLiIYYWBEWyp2IRJKfG4adWITR35qJBZOfnsadGNHWw/w644")
    embed.add_field(name="#礦工", value="按下這個標籤【⛏️】", inline=True)
    embed.add_field(name="#啞巴", value="按下這個標籤【🫢】", inline=True)
    embed.add_field(name="#我們缺DJ", value="按下這個標籤【💿】", inline=True)
    embed.add_field(name="#開車車", value="按下這個標籤【🤵‍♂】", inline=True)
    embed.add_field(name="美女", value="按下這個標籤【💃】", inline=True)
    embed.add_field(name="帥哥", value="按下這個標籤【🕺】", inline=True)
    embed.add_field(name="處男", value="按下這個標籤【🤮】", inline=True)
    embed.add_field(name="大GG", value="按下這個標籤【👃】", inline=True)
    embed.set_footer(text="\n\n嗯哼嗯哼嗯亨嗯亨")
    await ctx.send(embed=embed)

@bot.event
async def on_raw_reaction_add(payload: discord.raw_models.RawReactionActionEvent):
    
    if (payload.channel_id == 1026408101752090665 and payload.message_id == 1027410329833066576):
        guild = await bot.fetch_guild(payload.guild_id) #print(guild) 學術探討研究群
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reactions = str(payload.emoji)
        user_object = payload.member
        botlog().debug(message)
        role_id = know_emoji_find_id(reactions)
        if role_id != 0:
            role = user_object.guild.get_role(role_id)
            await user_object.add_roles(role, atomic=True)
            name = know_id_find_name(role_id)
            serverlog().info("已幫 " + str(guild) + ":" + str(user_object) + " 加入身分組 " + name + " (" + str(role_id) + ")") 

#payload.member only works with on_raw_reaction_add()
@bot.event
async def on_raw_reaction_remove(payload: discord.raw_models.RawReactionActionEvent):
    if (payload.channel_id == 1026408101752090665 and payload.message_id == 1027410329833066576): #限定只能在這個頻道的這則訊息
        guild = await bot.fetch_guild(payload.guild_id) #print(guild) 學術探討研究群
        user_object = await guild.fetch_member(payload.user_id) #print(user_object) brianoy
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reactions = str(payload.emoji)
        #guild_id = payload.guild_id
        botlog().debug(message)
        role_id = know_emoji_find_id(reactions)
        if role_id != 0:
            role = user_object.guild.get_role(role_id)
            await user_object.remove_roles(role, atomic=True)
            name = know_id_find_name(role_id)
            serverlog().info("已幫 " + str(guild) + ":" + str(user_object) + " 移除身分組 " + name + " (" + str(role_id) + ")") 
    
@bot.event
async def on_message(message: discord.message.Message):
    #print(type(message))
    if message.author.bot: #排除掉機器人、自己還有webhook傳的訊息
        pass
    else: #排除掉雜魚訊息後進入處理訊息模組
        #print(message)
        msg_pros_object = await message_process.message_process(message, bot) #訊息處理，在mod/message_process裡面
        try:
            #print(message.attachments[0]['url']) #尚未完成qr code 圖片點名
            pass
        except IndexError:
            pass
        if msg_pros_object != False: #msg_pros_object內部有東西才channel.send，否則將會raise error
            await message.channel.send(msg_pros_object)
        await bot.process_commands(message) #加了這行才可以監聽on_message順便還有指令的功能，要不然一開始on_message會override bot的command權限

@bot.event
async def on_voice_state_update(member, before, after):
    voice_chat_log(member, before, after)



 #--------------------------------------------------------------------------------------------

if __name__ == "__main__":
    '''
    serverlog().info('延遲開機: ')
    with alive_bar(300) as bar:
        for i in range(1,3):
            try:
                bar()
                time.sleep(0.1)
                pass
            except KeyboardInterrupt:
                serverlog().info('Ignored delay boot')
                break
            except Exception as e:
                serverlog().info(str(e))
        serverlog().info('自檢結束')
    '''
    #upgrade_chromedriver()
    
    bot.run(TOKEN) 
 #--------------------------------------------------------------------------------------------
