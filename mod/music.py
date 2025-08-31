import discord
#import hashlib
from pytube import YouTube


class music:
    def __init__(self):
        self.playlist_url = []

    async def add_play_list(self,url):
        self.playlist_url.append(url)

    async def download_music(self,url)->str:
        """
        @return False if everything is fine
        @return Str if something on fire
        """
        
        try:
            #hash = hashlib.sha1()
            #file_hash_name = hash.update(url.encode("utf-8"))
            #file_hash_name.hexdigest()

            yt = YouTube(url)
            #yt.streams.filter().get_audio_only().download(filename="music_cache/" + url[:11] + ".mp3")
            yt.streams.filter().get_audio_only().download(filename="play_music_cache.mp3")
            return False
        except Exception as e:
            if e.__class__.__name__ == "RegexMatchError" :
                return "RegexMatchError/網址不符合"
            elif e.__class__.__name__ == "AgeRestrictedError" :
                return "影片具有年齡限制，無法播放"
            elif e.__class__.__name__ == "ExtractError" :
                return "ExtractError/下載器錯誤"
            elif e.__class__.__name__ == "MembersOnly" :
                return "影片不對外開放，無法播放"
            elif e.__class__.__name__ == "RecordingUnavailable" :
                return "影片存檔不對外開放，無法播放"
            elif e.__class__.__name__ == "VideoUnavailable" :
                return "VideoUnavailable/影片錯誤，無法播放"
            elif e.__class__.__name__ == "VideoPrivate" :
                return "私人影片，無法播放"
            elif e.__class__.__name__ == "LiveStreamError" :
                return "LiveStreamError/無法播放直播"



    async def turn_on_player(self,bot,message):
        channel = message.author.voice.channel
        if not message.guild.voice_client in bot.voice_clients:
            connect = await channel.connect()
            return connect


    async def play_music(self,bot, message):
        if not message.author.voice: #使用者沒有加入語音頻道
            return False
        else:
            voice = discord.utils.get(bot.voice_clients, guild=message.guild)
            if voice == None: #voice.isplaying() attribute doesn't exist before connect
                print(voice)
                connect = await self.turn_on_player(bot,message)
                #after 建立在play下，而非ffmpeg
                audio = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="play_music_cache.mp3")
                connect.play(audio, after=lambda e: print('Player error: %s' % e) if e else bot.loop.create_task(self.play_music(bot, message)))
                #connect.play(audio)
                #await connect.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="play_music_cache.mp3"), after=lambda e: self.after_play_music(bot, message))
            else:
                print(voice) #<discord.voice_client.VoiceClient object at 0x0000027FE09BE020>
                voice.pause()
                audio = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="play_music_cache.mp3")
                voice.play(audio, after=lambda e: print('Player error: %s' % e) if e else bot.loop.create_task(self.play_music(bot, message)))
                #voice.play(audio)        
            return False
'''
    async def after_play_music(self,bot, message):
        connect = await self.turn_on_player(bot,message)
        #after 建立在play下，而非ffmpeg
        audio = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="play_music_cache.mp3")
        await connect.play(audio, after=lambda e: self.after_play_music(bot, message))
        return False
'''