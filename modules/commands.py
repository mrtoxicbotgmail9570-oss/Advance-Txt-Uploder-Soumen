import os
import re
import sys
import json
import time
from vars import CREDIT
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

# commands button
def register_commands_handlers(bot):
    # .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("cmd_command"))
    async def cmd(client, callback_query):
        user_id = callback_query.from_user.id
        first_name = callback_query.from_user.first_name
        caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to select Commands**"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚻 User", callback_data="user_command"), InlineKeyboardButton("🚹 Owner", callback_data="owner_command")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
        ])
        await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/8c148221d261c06e2102b-7164eb21e504cbefe3.jpg",
          caption=caption
        ),
        reply_markup=keyboard
        )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("user_command"))
    async def help_button(client, callback_query):
      user_id = callback_query.from_user.id
      first_name = callback_query.from_user.first_name
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Commands", callback_data="cmd_command")]])
      caption = (
            f"💥 𝐁𝐎𝐓𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒\n"
            f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n" 
            f"📌 𝗠𝗮𝗶𝗻 𝗙𝗲𝗮𝘁𝘂𝗿𝗲𝘀:\n\n"  
            f"➥ /start – 🫩Chek im i Alive?\n"
            f"➥ /stop – 🌼Cancel Running Task\n"
            f"➥ /y2t – YouTube to txt file Converter\n"  
            f"➥ /ytm – YouTube to mp3 audio downloader\n"  
            f"➥ /t2t – Message to txt file \n"
            f"➥ /t2h – txt file to html Converter\n"
            f"➥ /pdfrename - 📄Rename a PDF File\n"
            f"➥ /renamevideo - 🎥Rename a Video\n"
            f"➥ /setvideocover - 🎞️Set Photo for Global Video Cover\n"
            f"➥ /changecover - 🔄Change Cover of a Video\n"
            f"➥ /viewvideocover - 👁️View Current Video Cover\n"
            f"➥ /delvideocover - ✖️Delete Video Cover\n"
            f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ \n" 
            f"⚙️ 𝗧𝗼𝗼𝗹𝘀 & 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀: \n\n" 
            f"➥ /cookies – Update YT Cookies\n" 
            f"➥ /id – Get Chat/User ID\n"  
            f"➥ /info – User Details\n"  
            f"➥ /logs – View Bot Activity\n"
            f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
            f"💡 𝗡𝗼𝘁𝗲:\n\n"  
            f"• Send any link for auto-extraction\n"
            f"• Send direct .txt file for auto-extraction\n"
            f"• Supports batch processing\n\n"  
            f"╭────────⊰◆⊱────────╮\n"   
            f" ➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : {CREDIT} 💻\n"
            f"╰────────⊰◆⊱────────╯\n"
      )
    
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/3f0529e0a232d7a076a60-998260a13c34d2b7ea.jpg",
          caption=caption
        ),
        reply_markup=keyboard
        )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("owner_command"))
    async def help_button(client, callback_query):
      user_id = callback_query.from_user.id
      first_name = callback_query.from_user.first_name
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Commands", callback_data="cmd_command")]])
      caption = (
            f"👤 𝐁𝐨𝐭 𝐎𝐰𝐧𝐞𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬\n\n" 
            f"➥ /addauth xxxx – Add User ID\n" 
            f"➥ /rmauth xxxx – Remove User ID\n"  
            f"➥ /users – Total User List\n"  
            f"➥ /broadcast – For Broadcasting\n"  
            f"➥ /broadusers – All Broadcasting Users\n"  
            f"➥ /reset – Reset Bot\n"
            f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"  
            f"╭────────⊰◆⊱────────╮\n"   
            f" ➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : {CREDIT} 💻\n"
            f"╰────────⊰◆⊱────────╯\n"
      )
    
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/28eaaf6ec37903d4c0841-93d28f7433c8e62dc2.jpg",
          caption=caption
        ),
        reply_markup=keyboard
      )
  
