from mod.addlog import serverlog, botlog#不要用print()，而是用botlog().debug()或sever.info()等等
import discord

"""
這邊是語音紀錄處理module
包含加入語音聊天室離開聊天室
以及開關麥克風跟耳機的紀錄
"""
def voice_chat_log(member: discord.member.Member, before:discord.member.VoiceState, after:discord.member.VoiceState):
    """
    Args:
        bot (_type_): 其實沒有東西用到它
        member (_type_): _description_
        before (_type_): 變化前
        after (_type_): 變化後
    """
    before_channel = str(before.channel) # str 來的語音聊天室
    after_channel = str(after.channel) # str 去的語音聊天室
    guild = str(member.guild.name) # str 學術探討研究群
    member = str(member) # str brianoy
    
    if before_channel == "None" :
        serverlog().info(guild + " : " + member + " 加入了 " + after_channel)
    elif after_channel == "None" :
        serverlog().info(guild + " : " + member + " 離開了 " + before_channel)
    elif before_channel == after_channel:
        member_voice_status(guild, member, before, after) 
    else:
        serverlog().info(guild + " : " + member + " 從 " + before_channel + " 跑到了 " + after_channel)

def member_voice_status(guild: str, member: discord.member.Member, before:discord.member.VoiceState, after:discord.member.VoiceState):
    if before.self_mute != after.self_mute:
        if before.self_mute == True:
            serverlog().info(guild + " : " + member + " 開啟麥克風")
        else:
            serverlog().info(guild + " : " + member + " 關閉麥克風")

            
    if before.self_deaf != after.self_deaf:
        if before.self_deaf == True:
            serverlog().info(guild + " : " + member + " 開啟耳機")
        else:
            serverlog().info(guild + " : " + member + " 關閉耳機")

    # 這邊設計雙if 
    # 因為關閉耳機的同時也會關閉麥克風，會造成若同時開起麥克風跟耳機會只出現開啟麥克風


    elif before.self_stream != after.self_stream:
        if before.self_stream == True:
            serverlog().info(guild + " : " + member + " 關閉直播")
        else:
            serverlog().info(guild + " : " + member + " 開啟直播")
            
    elif before.suppress != after.suppress:
        if before.suppress == True:
            serverlog().warning(guild + " : " + member + " 所以這到底是啥1")#解除伺服器端禁麥 only for StageChannel
        else:
            serverlog().warning(guild + " : " + member + " 所以這到底是啥2")#被伺服器端禁麥 only for StageChannel
            
    elif before.requested_to_speak_at != after.requested_to_speak_at:
        if before.requested_to_speak_at == True:
            serverlog().info(guild + " : " + member + " 要求講話")
        else:
            serverlog().info(guild + " : " + member + " 無要求講話")
    else:
        pass
