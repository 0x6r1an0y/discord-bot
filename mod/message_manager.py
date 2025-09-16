"""
訊息管理器模組 - 提供智能快取的訊息編輯功能
"""

import discord
from typing import Union
from .addlog import serverlog


class MessageManager:
    """訊息管理器 - 提供智能快取的訊息編輯功能"""
    
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.message_channel_cache = {}  # {message_id: channel_object}
    
    async def update_message(self, msg_id: int, content: Union[str, discord.Embed]) -> bool:
        """
        @overload
        統一的訊息更新方法 - 支援函式多載
        根據傳入參數類型自動選擇更新方式：
        - 如果是 str：更新文字內容
        - 如果是 discord.Embed：更新嵌入式訊息
        
        Args:
            msg_id: 待編輯的訊息ID
            content: 要更新的內容 (str 或 discord.Embed)
            
        Returns:
            bool: 更新成功返回True，失敗返回False
        """ 
        if isinstance(content, str):
            # serverlog().debug(f"偵測到文字內容，使用 content 模式更新訊息 {msg_id}")
            return await self._update_message_content(msg_id, content)
        elif isinstance(content, discord.Embed):
            # serverlog().debug(f"偵測到 Embed 物件，使用 embed 模式更新訊息 {msg_id}")
            return await self._update_message_embed(msg_id, content)
        else:
            serverlog().error(f"不支援的內容類型: {type(content)}，僅支援 str 或 discord.Embed")
            return False
    
    async def _update_message_content(self, msg_id: int, edit_msg: str) -> bool:
        """
        更新指定訊息的文字內容（私有方法）
        
        Args:
            msg_id: 待編輯的訊息ID
            edit_msg: 要改的訊息內容
            
        Returns:
            bool: 更新成功返回True，失敗返回False
        """
        try:
            # 先檢查快取中是否有該訊息的channel
            if msg_id in self.message_channel_cache:
                channel = self.message_channel_cache[msg_id]
                # serverlog().debug(f"使用快取的channel: {channel.name}")
            else:
                # 如果快取中沒有，需要搜尋該訊息所在的channel
                channel = await self._find_message_channel(msg_id)
                if not channel:
                    serverlog().error(f"無法找到訊息 {msg_id} 所在的頻道")
                    return False
            
            # 獲取並更新訊息
            message = await channel.fetch_message(msg_id)
            await message.edit(content=edit_msg)
            # serverlog().info(f"成功更新訊息 {msg_id}: {edit_msg[:50]}...")
            return True
            
        except discord.NotFound:
            serverlog().error(f"訊息 {msg_id} 不存在")
            # 從快取中移除無效的訊息
            self.remove_from_cache(msg_id)
            return False
        except discord.Forbidden:
            serverlog().error(f"沒有權限編輯訊息 {msg_id}")
            return False
        except Exception as e:
            serverlog().error(f"更新訊息 {msg_id} 時發生錯誤: {e}")
            return False
    
    async def _update_message_embed(self, msg_id: int, embed: discord.Embed) -> bool:
        """
        更新指定訊息的embed內容（私有方法）
        
        Args:
            msg_id: 待編輯的訊息ID
            embed: 要更新的embed物件
            
        Returns:
            bool: 更新成功返回True，失敗返回False
        """
        try:
            # 先檢查快取中是否有該訊息的channel
            if msg_id in self.message_channel_cache:
                channel = self.message_channel_cache[msg_id]
                # serverlog().debug(f"使用快取的channel: {channel.name}")
            else:
                # 如果快取中沒有，需要搜尋該訊息所在的channel
                channel = await self._find_message_channel(msg_id)
                if not channel:
                    serverlog().error(f"無法找到訊息 {msg_id} 所在的頻道")
                    return False
            
            # 獲取並更新訊息
            message = await channel.fetch_message(msg_id)
            await message.edit(embed=embed)
            # serverlog().info(f"成功更新訊息 {msg_id} 的embed")
            return True
            
        except discord.NotFound:
            serverlog().error(f"訊息 {msg_id} 不存在")
            # 從快取中移除無效的訊息
            self.remove_from_cache(msg_id)
            return False
        except discord.Forbidden:
            serverlog().error(f"沒有權限編輯訊息 {msg_id}")
            return False
        except Exception as e:
            serverlog().error(f"更新訊息 {msg_id} 的embed時發生錯誤: {e}")
            return False
    
    async def update_message_content_and_embed(self, msg_id: int, content: str = None, embed: discord.Embed = None) -> bool:
        """
        同時更新訊息的內容和embed
        
        Args:
            msg_id: 待編輯的訊息ID
            content: 要更新的訊息內容 (可選)
            embed: 要更新的embed物件 (可選)
            
        Returns:
            bool: 更新成功返回True，失敗返回False
        """
        try:
            # 先檢查快取中是否有該訊息的channel
            if msg_id in self.message_channel_cache:
                channel = self.message_channel_cache[msg_id]
                # serverlog().debug(f"使用快取的channel: {channel.name}")
            else:
                # 如果快取中沒有，需要搜尋該訊息所在的channel
                channel = await self._find_message_channel(msg_id)
                if not channel:
                    serverlog().error(f"無法找到訊息 {msg_id} 所在的頻道")
                    return False
            
            # 獲取並更新訊息
            message = await channel.fetch_message(msg_id)
            await message.edit(content=content, embed=embed)
            # serverlog().info(f"成功更新訊息 {msg_id} 的內容和embed")
            return True
            
        except discord.NotFound:
            serverlog().error(f"訊息 {msg_id} 不存在")
            # 從快取中移除無效的訊息
            self.remove_from_cache(msg_id)
            return False
        except discord.Forbidden:
            serverlog().error(f"沒有權限編輯訊息 {msg_id}")
            return False
        except Exception as e:
            serverlog().error(f"更新訊息 {msg_id} 時發生錯誤: {e}")
            return False
    
    async def _find_message_channel(self, msg_id: int):
        """
        私有方法：搜尋訊息所在的頻道並加入快取
        
        Args:
            msg_id: 要搜尋的訊息ID
            
        Returns:
            discord.TextChannel or None: 找到的頻道物件，找不到則返回None
        """
        # serverlog().debug(f"搜尋訊息 {msg_id} 所在的頻道...")
        
        for guild in self.bot.guilds:
            for guild_channel in guild.text_channels:
                try:
                    message = await guild_channel.fetch_message(msg_id)
                    if message:
                        # 將找到的channel加入快取
                        self.message_channel_cache[msg_id] = guild_channel
                        serverlog().info(f"找到訊息 {msg_id} 在頻道 {guild_channel.name}，已加入快取")
                        return guild_channel
                except discord.NotFound:
                    continue
                except discord.Forbidden:
                    continue
                except Exception as e:
                    serverlog().error(f"搜尋訊息時發生錯誤: {e}")
                    continue
        
        return None
    
    def add_to_cache(self, msg_id: int, channel):
        """
        手動將訊息和頻道的映射加入快取
        
        Args:
            msg_id: 訊息ID
            channel: 頻道物件
        """
        self.message_channel_cache[msg_id] = channel
        serverlog().debug(f"已將訊息 {msg_id} 和頻道 {channel.name} 的映射加入快取")
    
    def remove_from_cache(self, msg_id: int):
        """
        從快取中移除特定訊息
        
        Args:
            msg_id: 要移除的訊息ID
        """
        if msg_id in self.message_channel_cache:
            del self.message_channel_cache[msg_id]
            serverlog().debug(f"已從快取中移除訊息 {msg_id}")
    
    def clear_cache(self):
        """清除所有快取"""
        self.message_channel_cache.clear()
        serverlog().info("已清除訊息快取")
    
    def get_cache_info(self) -> dict:
        """
        獲取快取資訊
        
        Returns:
            dict: 包含快取統計資訊的字典
        """
        return {
            "cached_messages": len(self.message_channel_cache),
            "message_ids": list(self.message_channel_cache.keys()),
            "channels": [channel.name for channel in self.message_channel_cache.values()]
        }
    
    def is_cached(self, msg_id: int) -> bool:
        """
        檢查訊息是否已快取
        
        Args:
            msg_id: 訊息ID
            
        Returns:
            bool: 已快取返回True，否則返回False
        """
        return msg_id in self.message_channel_cache
