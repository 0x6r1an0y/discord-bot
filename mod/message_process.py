from auto_roll_call.roll_call import auto_roll_call
from mod.addlog import serverlog, botlog#不要用print()，而是用botlog().debug()或severlog().info()等等
from mod.music import music
from discord.message import Message
check_rollcall_url = ["https://itouch.cycu.edu.tw" , "active_system/query_course/learning" , "?act_no="]
check_music_url = ["https://youtu.be/" , "https://www.youtube.com/watch?v="]
class message_process:
    async def message_process(message:Message, bot):
        botlog().debug(" "+ str(message.author) + "/" +str(message.guild.name) + " : " + str(message.channel) + " : " + str(message.content))
        #print(message.content)
        #print(len(message.content))
        #all() vs. any()
        if all(x in message.content for x in check_rollcall_url):
        #if ["https://itouch.cycu.edu.tw" , "active_system/query_course/learning" , "?act_no="] in message.content:
            try:
                roll_call_obj = auto_roll_call()
                roll_call_obj.__init__() #並且一定要呼叫建構子.....不然他會一直說找不到url_login的arrgument...
                return roll_call_obj.url_login(message.content)
            except Exception as E:
                print(str(E))
                return "點名錯誤，請再試一次" + "\n" + str(E)
        elif any(x in message.content for x in check_music_url):
            music_obj = music()
            err_msg = await music_obj.download_music(message.content)
            if err_msg == False:
                err_msg = await music_obj.play_music(bot, message)
            else:
                pass
            return err_msg

        else:
            return False
    
