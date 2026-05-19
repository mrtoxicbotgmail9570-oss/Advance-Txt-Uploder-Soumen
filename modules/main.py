import os
import re
import sys
import json
import time
import pytz
import asyncio
import requests
import subprocess
import random
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InputMediaPhoto
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
import globals
from logs import logging
from html_handler import register_html_handlers
from drm_handler import register_drm_handlers
from pdf_rename import register_pdf_rename_handlers
from pdfthumb import register_pdfthumb_handlers
from video_cover import register_video_cover_handlers, load_global_videocover_on_start
from video_rename import register_video_rename_handlers
from text_handler import register_text_handlers
from features import register_feature_handlers
from upgrade import register_upgrade_handlers
from commands import register_commands_handlers
from settings import register_settings_handlers
from broadcast import register_broadcast_handlers
from youtube_handler import register_youtube_handlers
from authorisation import register_authorisation_handlers
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, AUTH_USERS, TOTAL_USERS, cookies_file_path
import user_store
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

# ── Random image list ────────────────────────────────────────────────────────
image_list = [
    "https://graph.org/file/417cc7326cab9036c0152-f6a281db2a6975dfa9.jpg",
    "https://graph.org/file/033121ad32291bcaddd01-d91ae4a1f7ca9378fc.jpg",
    "https://graph.org/file/45f48779e0aa39709d1e8-4c024567d60f6ec5c2.jpg",
    "https://graph.org/file/6ccdd92af77784c9d367e-a4ba6f10456656bbbd.jpg",
    "https://graph.org/file/b23084c3e9124e14e18ec-d385f8f9c8b1635a2e.jpg",
    "https://graph.org/file/29c4511ee7a4653d22fe1-67906a2a8392895644.jpg",
    "https://graph.org/file/b45300f1cd068ad8f1895-fa23a3a1ad25789597.jpg",
]
# ─────────────────────────────────────────────────────────────────────────────

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ All Commands", callback_data="cmd_command")],
            [InlineKeyboardButton("💎 All Features", callback_data="feat_command"), InlineKeyboardButton("⚙️ Settings", callback_data="setttings")],
            [InlineKeyboardButton("💳 Premium Plans", callback_data="upgrade_command")],
            [InlineKeyboardButton(text="🔍Developer", url="https://t.me/CinderellaContactBot"), InlineKeyboardButton(text="👑 Owner", url="https://t.me/MR_Toxic_1")],
            [InlineKeyboardButton(text="💥Cinderella Rename", url="https://t.me/Cinderella_renameBot"), InlineKeyboardButton(text="💥Cinderella String", url="https://t.me/Cinderella_StringBot")],
        ])      

@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    user_id = m.chat.id
    if user_id not in TOTAL_USERS:
        TOTAL_USERS.append(user_id)
    user_store.register_user(m.chat.id)
    user = await bot.get_me()
    mention = user.mention
    if m.chat.id in AUTH_USERS:
        caption = (
            f"𝐇𝐞𝐥𝐥𝐨 𝐃𝐞𝐚𝐫👑!\n\n"
            f"➠ 𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭\n\n"
            f"➠ Can Extract Videos & PDFs From Your Text File and Upload to Telegram!\n\n"
            f"➠ For Guide Use button - **✨ Commands** 📖\n\n"
            f"➠ 𝐌𝐚𝐝𝐞 𝐁𝐲 : [{CREDIT}](tg://openmessage?user_id={OWNER}) 🦁"
        )
    else:
        caption = (
            f"𝐇𝐞𝐥𝐥𝐨🫣 **{m.from_user.first_name}** 👋!\n\n"
            f"➠ 𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭\n\n"
            f"➠ Can Extract Videos & PDFs From Your Text File and Upload to Telegram!\n\n"
            f"**You are currently using the free version.** 🆓\n"
            f"**Want to get Premium so let's started? Press /id**\n\n"
            f"💬 Contact: [{CREDIT}](tg://openmessage?user_id={OWNER}) to Get the Premium Subscription ! 🔓\n"
        )
    await bot.send_photo(
        chat_id=m.chat.id,
        photo=random.choice(image_list),
        caption=caption,
        reply_markup=keyboard
    )
    
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_callback_query(filters.regex("back_to_main_menu"))
async def back_to_main_menu(client, callback_query):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    caption = (
        f"𝐇𝐞𝐥𝐥𝐨 **{first_name}** 👋!\n\n"
        f"➠ 𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭\n\n"
        f"➠ 𝐁𝐲 : [{CREDIT}](tg://openmessage?user_id={OWNER})"
    )
    
    await callback_query.message.edit_media(
      InputMediaPhoto(
        media=random.choice(image_list),
        caption=caption
      ),
      reply_markup=keyboard
    )
    await callback_query.answer()

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Send to Owner💫", url=f"tg://openmessage?user_id={OWNER}")]])
    chat_id = message.chat.id
    text = f"<blockquote expandable><b>The ID of this chat id is:</b></blockquote>\n`{chat_id}`"
    
    if str(chat_id).startswith("-100"):
        await message.reply_text(text)
    else:
        await message.reply_text(text, reply_markup=keyboard)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, update: Message):
    text = (
        f"╭────────────────╮\n"
        f"│✨ **Your Telegram Info**✨ \n"
        f"├────────────────\n"
        f"├🔹**Your Name :** `{update.from_user.first_name} {update.from_user.last_name if update.from_user.last_name else 'None'}`\n"
        f"├🔹**User Name :** {('@' + update.from_user.username) if update.from_user.username else 'None'}\n"
        f"├🔹**User ID:** `{update.from_user.id}`\n"
        f"├🔹**Your Profile :** {update.from_user.mention}\n"
        f"╰────────────────╯"
    )    
    await update.reply_text(        
        text=text,
        disable_web_page_preview=True
    )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["logs"]))
async def send_logs(client: Client, m: Message):  # Correct parameter name
    try:
        with open("logs.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"**Error sending logs:**\n<blockquote>{e}</blockquote>")

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command(["reset"]))
async def restart_handler(_, m):
    if m.chat.id != OWNER:
        return
    else:
        await m.reply_text("𝐁𝐨𝐭 𝐢𝐬 𝐑𝐞𝐬𝐞𝐭𝐢𝐧𝐠...", True)
        os.execl(sys.executable, sys.executable, *sys.argv)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
@bot.on_message(filters.command("stop") & filters.private)
async def cancel_handler(client: Client, m: Message):
    if m.chat.id not in AUTH_USERS:
        print(f"User ID not in AUTH_USERS", m.chat.id)
        await bot.send_message(
            m.chat.id, 
            f"<blockquote>__**🙆🏿‍♀️Oopss! You are not a Premium member**__\n"
            f"__**Please Upgrade Your Plan**__\n"
            f"__**Send me your user id for authorization**__\n"
            f"__**Your User id** __- `{m.chat.id}`</blockquote>\n\n"
        )
    else:
        if globals.processing_request:
            globals.cancel_requested = True
            await m.delete()
            cancel_message = await m.reply_text("**🚦 Process cancel request received. Stopping after current process...**")
            await asyncio.sleep(30)  # 30 second wait
            await cancel_message.delete()
        else:
            await m.reply_text("**⚡ No active process to cancel.**")


#=================================================================

register_text_handlers(bot)
register_html_handlers(bot)
register_feature_handlers(bot)
register_settings_handlers(bot)
register_upgrade_handlers(bot)
register_commands_handlers(bot)
register_broadcast_handlers(bot)
register_youtube_handlers(bot)
register_authorisation_handlers(bot)
register_pdf_rename_handlers(bot)  # MUST be before drm_handlers so /pdfrename is caught first
register_pdfthumb_handlers(bot)    # PDF Thumbnail commands: /setpdfthumb /viewpdfthumb /delpdfthumb
register_video_cover_handlers(bot) # Video Cover commands: /setvideocover /viewvideocover /delvideocover
register_video_rename_handlers(bot) # Video Rename command: /renamevideo
register_drm_handlers(bot)
#==================================================================

def notify_owner():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": OWNER,
        "text": "𝐁𝐨𝐭 𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 ✅"
    }
    requests.post(url, data=data)

def reset_and_set_commands():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"

    # General users ke liye commands
    general_commands = [
        {"command": "start", "description": "✅ Check Alive the Bot"},
        {"command": "stop", "description": "🚫 Stop the ongoing process"},
        {"command": "id", "description": "🆔 Get Your ID"},
        {"command": "info", "description": "ℹ️ Check Your Information"},
        {"command": "cookies", "description": "📁 Upload YT Cookies"},
        {"command": "y2t", "description": "🔪 YouTube → .txt Converter"},
        {"command": "ytm", "description": "🎶 YouTube → .mp3 downloader"},
        {"command": "t2t", "description": "📟 Text → .txt Generator"},
        {"command": "t2h", "description": "🌐 .txt → .html Converter"},
        {"command": "pdfrename", "description": "📄 Rename a PDF file"},
        {"command": "renamevideo", "description": "🎥 Rename a Video file"},
        {"command": "setvideocover", "description": "🖼️ Set Global Video Cover"},
        {"command": "changecover", "description": "🔄 Change Cover of a Video"},
        {"command": "viewvideocover", "description": "👁️ View Current Video Cover"},
        {"command": "delvideocover", "description": "❌ Delete Video Cover"},
        {"command": "logs", "description": "👁️ View Bot Activity"},
    ]
    # Owner ke liye extra commands
    owner_commands = general_commands + [
        {"command": "broadcast", "description": "📢 Broadcast to All Users"},
        {"command": "broadusers", "description": "👨‍❤️‍👨 All Broadcasting Users"},
        {"command": "addauth", "description": "▶️ Add Authorisation"},
        {"command": "rmauth", "description": "⏸️ Remove Authorisation "},
        {"command": "users", "description": "👨‍👨‍👧‍👦 All Premium Users"},
        {"command": "reset", "description": "✅ Reset the Bot"}
    ]

    # General users ke liye set commands (scope default)
    requests.post(url, json={
        "commands": general_commands,
        "scope": {"type": "default"},
        "language_code": "en"
    })

    # Owner ke liye set commands (scope user)
    requests.post(url, json={
        "commands": owner_commands,
        "scope": {"type": "chat", "chat_id": OWNER},  # OWNER variable me chat id hona chahiye
        "language_code": "en"
    })
    
if __name__ == "__main__":
    load_global_videocover_on_start()
    reset_and_set_commands()
    notify_owner() 

bot.run()
