import os
import re
import sys
import json
import time
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

# Features button
def register_feature_handlers(bot):
    @bot.on_callback_query(filters.regex("feat_command"))
    async def feature_button(client, callback_query):
        caption = "**✨ My Premium BOT Features :**"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📌 Auto Pin Batch Name", callback_data="pin_command")],
            [InlineKeyboardButton("💧 Watermark", callback_data="watermark_command"), InlineKeyboardButton("🔄 Reset", callback_data="reset_command")],
            [InlineKeyboardButton("🖨️ Bot Working Logs", callback_data="logs_command")],
            [InlineKeyboardButton("🖋️ File Name", callback_data="custom_command"), InlineKeyboardButton("🏷️ Title", callback_data="titlle_command")],
            [InlineKeyboardButton("🎥 YouTube", callback_data="yt_command")],
            [InlineKeyboardButton("🌐 HTML", callback_data="html_command")],
            [InlineKeyboardButton("📝 Text File", callback_data="txt_maker_command"), InlineKeyboardButton("📢 Broadcast", callback_data="broadcast_command")],
            [InlineKeyboardButton("📄 PDF Features", callback_data="pdf_features_command")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
        ])
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/d94225198c49f4837ad6d-956835edec68f686bb.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
  
    @bot.on_callback_query(filters.regex("pin_command"))
    async def pin_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
        caption = f"**Auto Pin 📌 Batch Name :**\n\nAutomatically Pins the Batch Name in Channel or Group, If Starting from the First Link."
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/4f489f48098e89b7240b2-0c35f0c5a758db2cb1.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

    @bot.on_callback_query(filters.regex("watermark_command"))
    async def watermark_button(client, callback_query):
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
      caption = f"**Custom Watermark :**\n\nSet Your Own Custom Watermark on Videos for Added Personalization."
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/45f48779e0aa39709d1e8-4c024567d60f6ec5c2.jpg",
          caption=caption
          ),
          reply_markup=keyboard
      )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("reset_command"))
    async def restart_button(client, callback_query):
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
      caption = f"**🔄 Reset Command:**\n\nIf You Want to Reset or Restart Your Bot, Simply Use Command /reset."
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/033121ad32291bcaddd01-d91ae4a1f7ca9378fc.jpg",
          caption=caption
          ),
          reply_markup=keyboard
      )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("logs_command"))
    async def pin_button(client, callback_query):
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
      caption = f"**🖨️ Bot Working Logs:**\n\n◆/logs - Bot Send Working Logs in .txt File."
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/29c4511ee7a4653d22fe1-67906a2a8392895644.jpg",
          caption=caption
          ),
          reply_markup=keyboard
        )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("custom_command"))
    async def custom_button(client, callback_query):
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
      caption = f"**🖋️ Custom File Name:**\n\nSupport for Custom Name before the File Extension.\nAdd name ..when txt is uploading"
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/b45300f1cd068ad8f1895-fa23a3a1ad25789597.jpg",
          caption=caption
          ),
          reply_markup=keyboard
      )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("titlle_command"))
    async def titlle_button(client, callback_query):
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
      caption = f"**Custom Title Feature :**\nAdd and customize titles at the starting\n**NOTE 📍 :** The Titile must enclosed within (Title), Best For appx's .txt file."
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/b67a919df868cbb82b3cb-131aaff80361c5af6e.jpg",
          caption=caption
          ),
          reply_markup=keyboard
      )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("broadcast_command"))
    async def pin_button(client, callback_query):
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
      caption = f"**📢 Broadcasting Support:**\n\n◆/broadcast - 📢 Broadcast to All Users.\n◆/broadusers - 👁️ To See All Broadcasting User"
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/8c148221d261c06e2102b-7164eb21e504cbefe3.jpg",
          caption=caption
          ),
          reply_markup=keyboard
      )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("txt_maker_command"))
    async def editor_button(client, callback_query):
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
      caption = f"**🤖 Available Commands 🗓️**\n◆/t2t for text to .txt file\n"
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/3f0529e0a232d7a076a60-998260a13c34d2b7ea.jpg",
          caption=caption
          ),
          reply_markup=keyboard
      )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("yt_command"))
    async def y2t_button(client, callback_query):
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
      caption = f"**YouTube Commands:**\n\n◆/y2t - 🔪 YouTube Playlist → .txt Converter\n◆/ytm - 🎶 YouTube → .mp3 downloader\n\n<blockquote><b>◆YouTube → .mp3 downloader\n01. Send YouTube Playlist.txt file\n02. Send single or multiple YouTube links set\neg.\n`https://www.youtube.com/watch?v=xxxxxx\nhttps://www.youtube.com/watch?v=yyyyyy`</b></blockquote>"
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/28eaaf6ec37903d4c0841-93d28f7433c8e62dc2.jpg",
          caption=caption
          ),
          reply_markup=keyboard
      )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("html_command"))
    async def y2t_button(client, callback_query):
      keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]])
      caption = f"**HTML Commands:**\n\n◆/t2h - 🌐 .txt → .html Converter"
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/d94225198c49f4837ad6d-956835edec68f686bb.jpg",
          caption=caption
          ),
          reply_markup=keyboard
      )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

    @bot.on_callback_query(filters.regex("^pdf_features_command$"))
    async def pdf_features_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📄 PDF Rename", callback_data="pdfrename_command")],
            [InlineKeyboardButton("🖼️ PDF Thumbnail", callback_data="pdfthumb_command")],
            [InlineKeyboardButton("🔙 Back to Feature", callback_data="feat_command")]
        ])
        caption = (
            "**📄 PDF Features :**\n\n"
            "◆ **PDF Rename** — Rename any PDF file and re-upload.\n"
            "◆ **PDF Thumbnail** — ⚠️Temporary Unavailable."
        )
        await callback_query.message.edit_media(
            InputMediaPhoto(
                media="https://graph.org/file/b45300f1cd068ad8f1895-fa23a3a1ad25789597.jpg",
                caption=caption
            ),
            reply_markup=keyboard
        )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

    @bot.on_callback_query(filters.regex("^pdfrename_command$"))
    async def pdfrename_feat_button(client, callback_query):
      keyboard = InlineKeyboardMarkup([
          [InlineKeyboardButton("💥𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐑𝐞𝐜𝐚𝐩𝐭𝐢𝐨𝐧", url="https://t.me/Cinderella_recaptionBot"), InlineKeyboardButton("💥𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐒𝐭𝐫𝐢𝐧𝐠", url="https://t.me/Cinderella_StringBot")],
          [InlineKeyboardButton("🔙 Back to PDF Features", callback_data="pdf_features_command")]
      ])
      caption = (
          f"**📄 PDF Rename Feature:**\n\n"
          f"◆/pdfrename - Rename any PDF file.\n\n"
          f"<blockquote><b>How to use:</b>\n"
          f"1. Send /pdfrename command\n"
          f"2. Bot will ask you to send your PDF file\n"
          f"3. Then send the new name (without .pdf)\n"
          f"4. Bot renames and re-uploads with new name\n"
          f"✅ PDF Thumbnail (if set) is applied automatically.</blockquote>\n\n"
          f"Use Powerful Recaption Bot **@Cinderella_recaptionBot**\n"
          f"If you want to Generate your String Session so use **@Cinderella_StringBot**"
      )
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/b45300f1cd068ad8f1895-fa23a3a1ad25789597.jpg",
          caption=caption
          ),
          reply_markup=keyboard
      )

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

    @bot.on_callback_query(filters.regex("^pdfthumb_command$"))
    async def pdfthumb_feat_button(client, callback_query):
      keyboard = InlineKeyboardMarkup([
          [InlineKeyboardButton("💥𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐑𝐞𝐜𝐚𝐩𝐭𝐢𝐨𝐧", url="https://t.me/Cinderella_recaptionBot"), InlineKeyboardButton("💥𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐒𝐭𝐫𝐢𝐧𝐠", url="https://t.me/Cinderella_StringBot")],
          [InlineKeyboardButton("🔙 Back to PDF Features", callback_data="pdf_features_command")]
      ])
      caption = (
          "**🖼️ PDF Thumbnail Feature**\n\n"
          "⚠️ **Temporary Unavailable**\n"
          "This feature is not available in this Bot.\n\n"
          "Use Powerful Recaption Bot **@Cinderella_recaptionBot**\n"
          "If you want to Generate your String Session so use **@Cinderella_StringBot**"
      )
      await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/b45300f1cd068ad8f1895-fa23a3a1ad25789597.jpg",
          caption=caption
          ),
          reply_markup=keyboard
      )
