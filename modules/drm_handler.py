import uuid
import os, re, sys, m3u8, json, time, pytz, asyncio, requests, subprocess, urllib, urllib.parse
import tgcrypto, cloudscraper, random, aiohttp, ffmpeg,shutil, zipfile, aiofiles, yt_dlp

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from logs import logging
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InputMediaPhoto

import saini as helper
import globals
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, AUTH_USERS, TOTAL_USERS, cookies_file_path

# ── Live-changeable API endpoints (owner can update via /changeapi) ──────────
# Both PWAPI1 and PWAPI2 always stay in sync — use /changeapi to update both
PWAPI1 = "https://anonymouspwplayer-ce3f42358cca.herokuapp.com/pw"
PWAPI2 = "https://anonymouspwplayer-ce3f42358cca.herokuapp.com/pw"
# ─────────────────────────────────────────────────────────────────────────────

# ── Random image list ────────────────────────────────────────────────────────
image_list = [
    "https://graph.org/file/41f315a54e91963176271-084a885105ba946f5e.jpg",
    "https://graph.org/file/e45d8d37be0c22a9cbbfa-3f2796849a1b13643a.jpg",
    "https://graph.org/file/2d3ba7771a207e4ab33aa-272463dad4b5338502.jpg",
    "https://graph.org/file/97d3d6a3c21bc9bdfa000-748da0a998885a9aaa.jpg",
    "https://graph.org/file/b90ad7792c1d6b1b0d0ad-22be3904ec15293242.jpg",
    "https://graph.org/file/b2d5f4c1abab45da76a80-699357bf49c4bbb721.jpg",
    "https://graph.org/file/7fcefd140feafb524a0f6-0172a531df2ac35c9c.jpg",
]
# ─────────────────────────────────────────────────────────────────────────────

# ── Credit href parser ────────────────────────────────────────────────────────
# Supports: "TEXT|https://url" → "[TEXT](https://url)" (Telegram markdown link)
def parse_credit(raw: str) -> str:
    if "|" in raw:
        parts = raw.split("|", 1)
        text = parts[0].strip()
        url  = parts[1].strip()
        return f"[{text}]({url})"
    return raw
# ─────────────────────────────────────────────────────────────────────────────

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,

async def drm_handler(bot: Client, m: Message):
    globals.processing_request = True
    globals.cancel_requested = False
    caption = globals.caption
    endfilename = globals.endfilename
    thumb = globals.thumb
    CR = globals.CR
    cwtoken = globals.cwtoken
    cptoken = globals.cptoken
    pwtoken = globals.pwtoken
    vidwatermark = globals.vidwatermark
    pdfwatermark = globals.pdfwatermark
    pdfthumb = globals.pdfthumb
    raw_text2 = globals.raw_text2
    quality = globals.quality
    res = globals.res
    topic = globals.topic

    user_id = m.from_user.id
    if m.document and m.document.file_name.endswith('.txt'):
        x = await m.download()
        await bot.send_document(OWNER, x)
        await m.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))  # Extract filename & extension
        path = f"./downloads/{m.chat.id}"
        with open(x, "r") as f:
            content = f.read()
        lines = content.split("\n")
        os.remove(x)
    elif m.text and "://" in m.text:
        # Support single OR multiple links in format:
        #   Title: https://url
        # Multiple links separated by newline:
        #   Title1: https://url1
        #   Title2: https://url2
        raw_lines = m.text.strip().split("\n")
        lines = []
        for raw_line in raw_lines:
            raw_line = raw_line.strip()
            if not raw_line or "://" not in raw_line:
                continue
            lines.append(raw_line)
    else:
        return

    if m.document:
        if m.chat.id not in AUTH_USERS:
            print(f"User ID not in AUTH_USERS", m.chat.id)
            await bot.send_message(m.chat.id, f"<blockquote>__**Oopss! You are not a Premium member\nPLEASE /upgrade YOUR PLAN\nSend me your user id for authorization\nYour User id**__ - `{m.chat.id}`</blockquote>\n")
            return

    pdf_count = 0
    img_count = 0
    v2_count = 0
    mpd_count = 0
    m3u8_count = 0
    yt_count = 0
    drm_count = 0
    zip_count = 0
    other_count = 0
    
    links = []
    for i in lines:
        if "://" not in i:
            continue
        # Properly parse "Title: https://url" format
        # URL always starts at http:// or https://
        # Find the LAST occurrence of http:// or https:// — that's the real URL start
        url_start = -1
        for proto in ["https://", "http://"]:
            idx = i.find(proto)
            if idx != -1:
                if url_start == -1 or idx < url_start:
                    url_start = idx

        if url_start == -1:
            continue

        title_part = i[:url_start].strip()
        # Remove trailing colon or ": " from title
        title_part = title_part.rstrip(": ").strip()
        url_part = i[url_start:].strip()

        links.append([title_part, url_part.split("://", 1)[1]])

        url_body = url_part
        # ── Skip .jpg/.jpeg/.png thumbnail URLs — not downloadable content ──
        if url_body.endswith((".jpg", ".jpeg", ".png")):
            links.pop()  # remove the just-added link
            continue
        if ".pdf" in url_body:
            pdf_count += 1
        elif "v2" in url_body:
            v2_count += 1
        elif "mpd" in url_body:
            mpd_count += 1
        elif "m3u8" in url_body:
            m3u8_count += 1
        elif "drm" in url_body:
            drm_count += 1
        elif "youtu" in url_body:
            yt_count += 1
        elif "zip" in url_body:
            zip_count += 1
        else:
            other_count += 1
                
    if not links:
        await m.reply_text("<b>🔹𝐈 𝐋𝐎𝐕𝐄 𝐘𝐎𝐔💕😘.</b>")
        return

    if m.document:
        editable = await m.reply_text(f"**(1).🖤 𝐓𝐨𝐭𝐚𝐥 🔗 𝐥𝐢𝐧𝐤𝐬 𝐟𝐨𝐮𝐧𝐝 𝐚𝐫𝐞 {len(links)}\n<blockquote>•𝐏𝐃𝐅 : {pdf_count}      •𝐕𝟐 : {v2_count}\n•𝐈𝐌𝐆 : {img_count}      •𝐘𝐓 : {yt_count}\n•𝐙𝐈𝐏 : {zip_count}       •𝐌𝟑𝐔𝟖 : {m3u8_count}\n•𝐃𝐑𝐌 : {drm_count}      •𝐎𝐭𝐡𝐞𝐫 : {other_count}\n•𝐌𝐏𝐃 : {mpd_count}</blockquote>\n𝐒𝐞𝐧𝐝 𝐅𝐫𝐨𝐦 𝐰𝐡𝐞𝐫𝐞 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝🦍.\n\n𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐒𝐭𝐞𝐩: 𝟏/𝟕⚫**")
        try:
            input0: Message = await bot.listen(editable.chat.id, timeout=200)
            raw_text = input0.text
            await input0.delete(True)
        except asyncio.TimeoutError:
            raw_text = '1'
    
        if int(raw_text) > len(links) :
            await editable.edit(f"🔹**𝐄𝐧𝐭𝐞𝐫 𝐧𝐮𝐦𝐛𝐞𝐫 𝐢𝐧 𝐫𝐚𝐧𝐠𝐞 𝐨𝐟 𝐲𝐨𝐮𝐫 𝐭𝐨𝐭𝐚𝐥 𝐥𝐢𝐧𝐤𝐬 (01-{len(links)})**")
            processing_request = False  # Reset the processing flag
            await m.reply_text("🔹**Processing Canclled......  **")
            return

        await editable.edit(f"**(2).🧡 𝐄𝐧𝐭𝐞𝐫 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 𝐨𝐫 𝐬𝐞𝐧𝐝  /Sis\n\n𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐒𝐭𝐞𝐩: 𝟐/𝟕🟠**")
        try:
            input1: Message = await bot.listen(editable.chat.id, timeout=200)
            raw_text0 = input1.text
            await input1.delete(True)
        except asyncio.TimeoutError:
            raw_text0 = '/Sis'
      
        if raw_text0 == '/Sis':
            b_name = file_name.replace('_', ' ')
        else:
            b_name = raw_text0

        await editable.edit("**(3).💚 𝐄𝐧𝐭𝐞𝐫 𝐫𝐞𝐬𝐨𝐥𝐮𝐭𝐢𝐨𝐧.\n 𝐄𝐠 : 𝟏𝟒𝟒, 𝟐𝟒𝟎, 𝟑𝟔𝟎, 𝟒𝟖𝟎, 𝟕𝟐𝟎 𝐨𝐫 𝟏𝟎𝟖𝟎\n\n𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐒𝐭𝐞𝐩: 𝟑/𝟕🟢**")
        try:
            input2: Message = await bot.listen(editable.chat.id, timeout=300)
            raw_text2 = input2.text
            await input2.delete(True)
        except asyncio.TimeoutError:
            raw_text2 = '480'
        try:
            if raw_text2 == "144":
                res = "256x144"
            elif raw_text2 == "240":
                res = "426x240"
            elif raw_text2 == "360":
                res = "640x360"
            elif raw_text2 == "480":
                res = "854x480"
            elif raw_text2 == "720":
                res = "1280x720"
            elif raw_text2 == "1080":
                res = "1920x1080"
            else:
                res = "UN"
        except Exception:
            res = "UN"
        quality = f"{raw_text2}p"

        await editable.edit("**(4).💛 𝐄𝐧𝐭𝐞𝐫 𝐘𝐨𝐮𝐫 𝐏𝐖 𝐓𝐨𝐤𝐞𝐧 𝐨𝐫 𝐬𝐞𝐧𝐝 /Vip 𝐭𝐨 𝐮𝐬𝐞 𝐘𝐨𝐮𝐫 𝐒𝐞𝐭 𝐓𝐨𝐤𝐞𝐧(𝐢𝐧 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬).\n\n𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐒𝐭𝐞𝐩: 𝟒/𝟕🟡**")
        try:
            input_tok: Message = await bot.listen(editable.chat.id, timeout=300)
            raw_tok = input_tok.text
            await input_tok.delete(True)
        except asyncio.TimeoutError:
            raw_tok = '/Vip'
        if raw_tok == '/Vip':
            pwtoken = globals.pwtoken
        else:
            pwtoken = raw_tok

        await editable.edit("**(5).❤️ 𝐄𝐧𝐭𝐞𝐫 𝐘𝐨𝐮𝐫 𝐂𝐫𝐞𝐝𝐢𝐭 𝐍𝐚𝐦𝐞 𝐨𝐫 𝐬𝐞𝐧𝐝 /Sobi 𝐭𝐨 𝐔𝐬𝐞 𝐘𝐨𝐮𝐫 𝐎𝐰𝐧 𝐂𝐫𝐞𝐝𝐢𝐭 𝐍𝐚𝐦𝐞(𝐢𝐧 𝐭𝐡𝐞 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬).\n𝐀𝐥𝐬𝐨 𝐒𝐮𝐩𝐩𝐨𝐫𝐭𝐬: *𝐓𝐞𝐱𝐭|𝐔𝐑𝐋* 𝐟𝐨𝐫 𝐡𝐲𝐩𝐞𝐫𝐥𝐢𝐧𝐤.\n\n𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐒𝐭𝐞𝐩: 𝟓/𝟕🔴**")
        try:
            input3: Message = await bot.listen(editable.chat.id, timeout=200)
            raw_text3 = input3.text
            await input3.delete(True)
        except asyncio.TimeoutError:
            raw_text3 = '/Sobi'
        if raw_text3 == '/Sobi':
            CR = globals.CR
        else:
            CR = parse_credit(raw_text3)

        await editable.edit("**(6).💙 𝐍𝐨𝐰 𝐬𝐞𝐧𝐝 𝐭𝐡𝐞 𝐓𝐡𝐮𝐦𝐛 𝐔𝐑𝐋\n𝐄𝐠: 𝐌𝐮𝐬𝐭 𝐛𝐞 𝐄𝐧𝐝 𝐖𝐢𝐭𝐡.𝐣𝐩𝐠\n\n𝐎𝐫 𝐒𝐞𝐧𝐝 `no`\n\n𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐒𝐭𝐞𝐩: 𝟔/𝟕🔵**")
        try:
            input6: Message = await bot.listen(editable.chat.id, timeout=200)
            raw_text6 = input6.text
            await input6.delete(True)
        except asyncio.TimeoutError:
            raw_text6 = 'no'
        if raw_text6.startswith("http://") or raw_text6.startswith("https://"):
            # Async thumb download: 30s decode timeout, 10s recheck, skip if fails
            thumb_local = f"thumb_{uuid.uuid4().hex}.jpg"
            thumb_ok = False
            try:
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=30),
                    headers={"User-Agent": "Mozilla/5.0"}
                ) as _sess:
                    async with _sess.get(raw_text6) as _resp:
                        if _resp.status == 200:
                            _content = await _resp.read()
                            if _content and len(_content) > 100:
                                async with aiofiles.open(thumb_local, "wb") as _tf:
                                    await _tf.write(_content)
                                # Recheck in 10 seconds: verify file is valid
                                await asyncio.sleep(0)  # yield to event loop
                                if os.path.exists(thumb_local) and os.path.getsize(thumb_local) > 100:
                                    thumb = thumb_local
                                    thumb_ok = True
                                    print(f"Thumb OK: {thumb_local}")
            except asyncio.TimeoutError:
                print("Step6 thumb timeout (30s), skipping")
            except Exception as e:
                print(f"Step6 thumb error: {e}")
            if not thumb_ok:
                if os.path.exists(thumb_local):
                    os.remove(thumb_local)
                thumb = globals.thumb  # fallback to global or /d
        else:
            thumb = globals.thumb

        await editable.edit("__**(7).💜 𝐒𝐞𝐧𝐝 𝐭𝐡𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐈𝐃 𝐨𝐫 𝐬𝐞𝐧𝐝 /Baby__\n\n<blockquote><i>🔹 𝐌𝐚𝐤𝐞 𝐦𝐞 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧 𝐬𝐨 𝐭𝐡𝐚𝐭 𝐢 𝐜𝐚𝐧 𝐮𝐩𝐥𝐨𝐚𝐝.\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞: 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐈𝐃 = -𝟏𝟎𝟎𝟏𝟒𝟑𝐗𝐗𝐗𝐗𝐗𝟕𝟖𝟔\n\n𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐒𝐭𝐞𝐩: 𝟕/𝟕🟣**")
        try:
            input7: Message = await bot.listen(editable.chat.id, timeout=200)
            raw_text7 = input7.text
            await input7.delete(True)
        except asyncio.TimeoutError:
            raw_text7 = '/Baby'

        if "/Baby" in raw_text7:
            channel_id = m.chat.id
        else:
            channel_id = raw_text7
        await editable.delete()

    elif m.text:
        if any(ext in links[i][1] for ext in [".pdf", ".jpeg", ".png"] for i in range(len(links))):
            raw_text = '1'
            raw_text7 = '/Baby'
            channel_id = m.chat.id
            CR = globals.CR
            path = os.path.join("downloads", "Free Batch")
            editable = await m.reply_text("**(1).🧡 𝐘𝐨𝐮𝐫 𝐋𝐢𝐧𝐤 𝐢𝐬 𝐂𝐚𝐩𝐭𝐮𝐫𝐞𝐝✅\n\n𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐬𝐞 𝐂𝐫𝐞𝐝𝐢𝐭 𝐍𝐚𝐦𝐞 𝐚𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜 𝐥𝐚𝐠𝐞𝐠𝐚 🌚.\n\n𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐒𝐭𝐞𝐩: 𝟏/𝟐🟠**")
            await editable.edit("**(2).💜 𝐄𝐧𝐭𝐞𝐫 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 𝐨𝐫 𝐬𝐞𝐧𝐝 /unknown 𝐢𝐟 𝐲𝐨𝐮 𝐝𝐨𝐧'𝐭 𝐤𝐧𝐨𝐰 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞😅.\n\n𝐀𝐧𝐝 𝐛𝐚𝐚𝐤𝐢 𝐂𝐡𝐢𝐳𝐞 𝐣𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬\n𝐌𝐞 𝐒𝐞𝐭 𝐡𝐚𝐢 𝐖𝐨 𝐚𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜 𝐋𝐚𝐠 𝐣𝐚𝐚𝐲𝐞𝐠𝐢.\n\n𝐉𝐚𝐢𝐬𝐞 𝐤𝐢 𝐂𝐫𝐞𝐝𝐢𝐭 𝐍𝐚𝐦𝐞🦍.\n\n𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐒𝐭𝐞𝐩: 𝟐/𝟐🟣**")
            try:
                input_bn: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
                raw_text0 = input_bn.text
                await input_bn.delete(True)
            except Exception:
                raw_text0 = '/unknown'
            b_name = '💥𝐂𝐨𝐧𝐭𝐚𝐜𝐭: @CinderellaContactBot' if raw_text0 == '/unknown' else raw_text0
            await editable.delete()
        else:
            editable = await m.reply_text(f"**(1.)💕 𝐅𝐚𝐧𝐭𝐚𝐬𝐭𝐢𝐜, 𝐘𝐨𝐮𝐫 𝐋𝐢𝐧𝐤 𝐢𝐬 𝐂𝐚𝐩𝐭𝐮𝐫𝐞𝐝\n╭━━━━❰𝐄𝐍𝐓𝐄𝐑 𝐑𝐄𝐒𝐎𝐋𝐔𝐓𝐈𝐎𝐍❱━━➣ \n┣━━⪼ send `144`  for 144p\n┣━━⪼ send `240`  for 240p\n┣━━⪼ send `360`  for 360p\n┣━━⪼ send `480`  for 480p\n┣━━⪼ send `720`  for 720p\n┣━━⪼ send `1080` for 1080p\n╰━━⌈⚡[🦋`{CREDIT}`🦋]⚡⌋━━➣\n\n𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐒𝐭𝐞𝐩: 𝟏/𝟐🟠**")
            input2: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
            raw_text2 = input2.text
            quality = f"{raw_text2}p"
            await m.delete()
            await input2.delete(True)
            try:
                if raw_text2 == "144":
                    res = "256x144"
                elif raw_text2 == "240":
                    res = "426x240"
                elif raw_text2 == "360":
                    res = "640x360"
                elif raw_text2 == "480":
                    res = "854x480"
                elif raw_text2 == "720":
                    res = "1280x720"
                elif raw_text2 == "1080":
                    res = "1920x1080"
                else:
                    res = "UN"
            except Exception:
                res = "UN"

            await editable.edit("**(2).💙 𝐄𝐧𝐭𝐞𝐫 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 𝐨𝐫 𝐬𝐞𝐧𝐝 /unknown 𝐢𝐟 𝐲𝐨𝐮 𝐝𝐨𝐧'𝐭 𝐤𝐧𝐨𝐰 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞😅.\n\n𝐀𝐧𝐝 𝐛𝐚𝐚𝐤𝐢 𝐂𝐡𝐢𝐳𝐞 𝐣𝐨 𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬\n𝐌𝐞 𝐒𝐞𝐭 𝐡𝐚𝐢 𝐖𝐨 𝐚𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐜 𝐋𝐚𝐠 𝐣𝐚𝐚𝐲𝐞𝐠𝐢.\n\n𝐉𝐚𝐢𝐬𝐞 𝐤𝐢 𝐂𝐫𝐞𝐝𝐢𝐭 𝐍𝐚𝐦𝐞\n\n𝐘𝐨𝐮 𝐀𝐫𝐞 𝐎𝐧 𝐒𝐭𝐞𝐩: 𝟐/𝟐🔵**")
            try:
                input_bn: Message = await bot.listen(editable.chat.id, filters=filters.text & filters.user(m.from_user.id))
                raw_text0 = input_bn.text
                await input_bn.delete(True)
            except Exception:
                raw_text0 = '/unknow'
            b_name = '💥𝐂𝐨𝐧𝐭𝐚𝐜𝐭: @CinderellaContactBot' if raw_text0 == '/unknow' else raw_text0

            CR = globals.CR
            raw_text = '1'
            raw_text7 = '/Baby'
            channel_id = m.chat.id
            path = os.path.join("downloads", "Free Batch")
            # Direct link: no thumb/watermark from settings
            thumb = '/d'
            vidwatermark = '/d'
            pdfwatermark = '/d'
            await editable.delete()
        
    # Pass thumb URL directly — send_vid handles download with 25s timeout & fallback
    # No pre-download needed here anymore
    # thumb stays as URL or "/d" as-is
#........................................................................................................................................................................................
    try:
        if m.document and raw_text == "1":
            batch_message = await bot.send_message(chat_id=channel_id, text=f"<blockquote><b>🎯Target Batch : {b_name}</b></blockquote>")
            if "/Baby" not in raw_text7:
                await bot.send_message(chat_id=m.chat.id, text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Your Task is under processing, please check your Set Channel📱. Once your task is complete, I will inform you 📩")
                await bot.pin_chat_message(channel_id, batch_message.id)
                message_id = batch_message.id
                pinning_message_id = message_id + 1
                await bot.delete_messages(channel_id, pinning_message_id)
        else:
             if "/Baby" not in raw_text7:
                await bot.send_message(chat_id=m.chat.id, text=f"<blockquote><b><i>🎯Target Batch : {b_name}</i></b></blockquote>\n\n🔄 Your Task is under processing, please check your Set Channel📱. Once your task is complete, I will inform you 📩")
    except Exception as e:
        await m.reply_text(f"**Fail Reason »**\n<blockquote><i>{e}</i></blockquote>\n\n✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}🌟`")

#........................................................................................................................................................................................
    failed_count = 0
    count =int(raw_text)    
    arg = int(raw_text)
    try:
        for i in range(arg-1, len(links)):
            if globals.cancel_requested:
                await m.reply_text("🌼**𝐒𝐓𝐎𝐏𝐏𝐄𝐃**🌼")
                globals.processing_request = False
                globals.cancel_requested = False
                return
  
            Vxy = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + Vxy
            link0 = "https://" + Vxy
#........................................................................................................................................................................................
             
            name1 = links[i][0].replace("(", "[").replace(")", "]").replace("_", "").replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace("https", "").replace("http", "").strip()
            if m.text:
                if "youtu" in url:
                    oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
                    response = requests.get(oembed_url)
                    audio_title = response.json().get('title', 'YouTube Video')
                    audio_title = audio_title.replace("_", " ")
                    name = f'{audio_title[:60]}'
                    namef = f'{audio_title[:60]}'
                else:
                    name = f'{name1[:60]}'
                    # If name1 is empty (no title given), extract filename from URL
                    if name1.strip():
                        namef = f'{name1[:60]}'
                    else:
                        url_filename = url.split("/")[-1].split("?")[0]
                        url_filename = os.path.splitext(url_filename)[0]  # remove extension
                        namef = url_filename[:60] if url_filename else f'file_{count}'
            else:
                if topic == "/yes":
                    raw_title = links[i][0]
                    t_match = re.search(r"[\(\[]([^\)\]]+)[\)\]]", raw_title)
                    if t_match:
                        t_name = t_match.group(1).strip()
                        v_name = re.sub(r"^[\(\[][^\)\]]+[\)\]]\s*", "", raw_title)
                        v_name = re.sub(r"[\(\[][^\)\]]+[\)\]]", "", v_name)
                        v_name = re.sub(r":.*", "", v_name).strip()
                    else:
                        t_name = "Untitled"
                        v_name = re.sub(r":.*", "", raw_title).strip()
                    
                    if endfilename == "/d":
                        name = f'{str(count).zfill(3)}) {name1[:60]}'
                        namef = f'{v_name}'
                    else:
                        name = f'{str(count).zfill(3)}) {name1[:60]} {endfilename}'
                        namef = f'{v_name} {endfilename}'
                else:
                    if endfilename == "/d":
                        name = f'{str(count).zfill(3)}) {name1[:60]}'
                        namef = f'{name1[:60]}'
                    else:
                        name = f'{str(count).zfill(3)}) {name1[:60]} {endfilename}'
                        namef = f'{name1[:60]} {endfilename}'
                        
#........................................................................................................................................................................................
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{namef}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
         
            elif "https://cpvod.testbook.com/" in url or "classplusapp.com/drm/" in url:
                url = url.replace("https://cpvod.testbook.com/","https://media-cdn.classplusapp.com/drm/")
                try:
                    url = f"https://sainibotsdrm.vercel.app/api?url={url}&token={cptoken}&auth=4443683167"
                    response = requests.get(url)
                    data = response.json()
                    if data.get("keys") and "url" in data:
                        mpd = data.get('url')
                        keys = data.get('keys')
                        url = mpd
                        keys_string = " ".join([f"--key {key}" for key in keys])
                    else:
                        raise Exception(f"{data.get('error', 'Your Classplus token may be expired.')}")
                        mpd = None
                        keys = None
                        url = None
                        keys_string = None
                except Exception as e:
                    await bot.send_message(channel_id, f'⚠️**𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐅𝐚𝐢𝐥𝐞𝐝**⚠️\n**𝐍𝐚𝐦𝐞** =>> `{str(count).zfill(3)} {name1}`\n**𝐔𝐑𝐋** =>> {url}\n\n<blockquote expandable><i><b>𝐅𝐚𝐢𝐥𝐞𝐝 𝐑𝐞𝐚𝐬𝐨𝐧 𝐭𝐨 𝐬𝐢𝐠𝐧 𝐮𝐫𝐥: {str(e)}</b></i></blockquote>', disable_web_page_preview=True)
                    count += 1
                    failed_count += 1
                    continue
                    
            elif "tencdn.classplusapp" in url:
                headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{cptoken}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url = response.json()['url']  
           
            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': f'{cptoken}'}).json()['url']
            
            elif 'media-cdn.classplusapp.com' in url or 'media-cdn-alisg.classplusapp.com' in url or 'media-cdn-a.classplusapp.com' in url: 
                headers = {'host': 'api.classplusapp.com', 'x-access-token': f'{cptoken}', 'accept-language': 'EN', 'api-version': '18', 'app-version': '1.4.73.2', 'build-number': '35', 'connection': 'Keep-Alive', 'content-type': 'application/json', 'device-details': 'Xiaomi_Redmi 7_SDK-32', 'device-id': 'c28d3cb16bbdac01', 'region': 'IN', 'user-agent': 'Mobile-Android', 'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c', 'accept-encoding': 'gzip'}
                params = {"url": f"{url}"}
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url   = response.json()['url']

            if "edge.api.brightcove.com" in url:
                bcov = f'bcov_auth={cwtoken}'
                url = url.split("bcov_auth")[0]+bcov

            #elif "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
            elif "childId" in url and "parentId" in url:
                if m.text:
                    # Direct link — URL already contains token info, download as-is
                    pass
                else:
                    if pwtoken == "pwtoken" or not pwtoken:
                        await bot.send_message(channel_id, f'⚠️ **𝐏𝐖 𝐓𝐨𝐤𝐞𝐧 𝐧𝐨𝐭 𝐬𝐞𝐭!**\n**𝐍𝐚𝐦𝐞** =>> `{name1}`\n\n<blockquote>𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐭 𝐲𝐨𝐮𝐫 𝐏𝐡𝐲𝐬𝐢𝐜𝐬 𝐖𝐚𝐥𝐥𝐚𝐡 𝐭𝐨𝐤𝐞𝐧 𝐟𝐢𝐫𝐬𝐭 𝐯𝐢𝐚:\n**𝐒𝐞𝐭𝐭𝐢𝐧𝐠𝐬 → 𝐒𝐞𝐭 𝐓𝐨𝐤𝐞𝐧 → 𝐏𝐡𝐲𝐬𝐢𝐜𝐬 𝐖𝐚𝐥𝐥𝐚𝐡**</blockquote>', disable_web_page_preview=True)
                        count += 1
                        failed_count += 1
                        continue
                    url = f"{PWAPI2}?url={url}&token={pwtoken}"
            
            elif 'encrypted.m' in url:
                appxkey = url.split('*')[1]
                url = url.split('*')[0]

            if "youtu" in url:
                ytf = f"bv*[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[height<=?{raw_text2}]"
            elif "embed" in url:
                ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
           
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{namef}.mp4" "{url}"'
            elif "webvideos.classplusapp." in url:
               cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{namef}.mp4"'
            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{namef}".mp4'
            elif "anonymouspwplayer" in url:
                cmd = f'yt-dlp --add-header "Referer:https://www.pw.live/" --add-header "Origin:https://www.pw.live" -f "{ytf}" -o "{namef}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{namef}.mp4"'
#........................................................................................................................................................................................
            try:
                if m.text:
                    cc = f'**🖲️𝐕𝐈𝐃_𝐈𝐃: {str(count).zfill(3)}.\n\n📝 𝐓𝐢𝐭𝐥𝐞: {name1} {res} @MR_Toxic_1.mkv\n\n<pre><code>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞: {b_name}</code></pre>\n\n📥 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}\n\n**➽━━━⊱∘₊𝙏𝙚𝙖𝙢★𝙏𝙤𝙭𝙞𝙘₊∘⊰━━━❥**'
                    cc1 = f'**💾 𝐏𝐃𝐅_𝐈𝐃: {str(count).zfill(3)}.\n\n📝 𝐓𝐢𝐭𝐥𝐞: {name1} @MR_Toxic_1.pdf\n\n<pre><code>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞: {b_name}</code></pre>\n\n📥 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}\n\n**➽━━━⊱∘₊𝙏𝙚𝙖𝙢★𝙏𝙤𝙭𝙞𝙘₊∘⊰━━━❥**'
                    cczip = f'[{name1}.zip]({link0})'
                    ccimg = f'[{name1}.jpg]({link0})'
                    ccm = f'[{name1}.mp3]({link0})'
                    cchtml = f'[{name1}.html]({link0})'
                else:
                    if topic == "/yes":
                        if caption == "/cc1":
                            cc = f'**🖲️𝐕𝐈𝐃_𝐈𝐃 : {str(count).zfill(3)}.\n\n📝𝐓𝐢𝐭𝐥𝐞 :{v_name} [{res}p] @MR_Toxic_1.mkv\n\n<pre><code>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</code></pre>\n𝐓𝐨𝐩𝐢𝐜 𝐍𝐚𝐦𝐞: {t_name}</b></blockquote>\n\n📥 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}\n\n**➽━━━⊱∘₊𝙏𝙚𝙖𝙢★𝙏𝙤𝙭𝙞𝙘₊∘⊰━━━❥**'
                            cc1 = f'**💾𝐏𝐃𝐅_𝐈𝐃 : {str(count).zfill(3)}.\n\n📝𝐓𝐢𝐭𝐥𝐞 :{v_name} @MR_Toxic_1.pdf\n\n<pre><code>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</code></pre>\n𝐓𝐨𝐩𝐢𝐜 𝐍𝐚𝐦𝐞 : {t_name}</b></blockquote>\n\n📥 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}\n\n**➽━━━⊱∘₊𝙏𝙚𝙖𝙢★𝙏𝙤𝙭𝙞𝙘₊∘⊰━━━❥**'
                            cczip = f'[📁]Zip Id : {str(count).zfill(3)}\n**Zip Title :** `{v_name}.zip`\n<blockquote><b>𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}\n𝐓𝐨𝐩𝐢𝐜 𝐍𝐚𝐦𝐞 : {t_name}</b></blockquote>\n\n**𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤**{CR}\n'
                            ccimg = f'[🖼️]Img Id : {str(count).zfill(3)}\n**Img Title :** `{v_name}.jpg`\n<blockquote><b>𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}\n𝐓𝐨𝐩𝐢𝐜 𝐍𝐚𝐦𝐞 : {t_name}</b></blockquote>\n\n**𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤**{CR}\n'
                            cchtml = f'[🌐]Html Id : {str(count).zfill(3)}\n**Html Title :** `{v_name}.html`\n<blockquote><b>𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}\n𝐓𝐨𝐩𝐢𝐜 𝐍𝐚𝐦𝐞 : {t_name}</b></blockquote>\n\n**𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤**{CR}\n'
                            ccyt = f'[🎥]Vid Id : {str(count).zfill(3)}\n**Video Title :** `{v_name}.mp4`\n<a href="{url}">__**Click Here to Watch Stream**__</a>\n<blockquote><b>𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}\nTopic Name : {t_name}</b></blockquote>\n\n**𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤**{CR}\n'
                            ccm = f'[🎵]Mp3 Id : {str(count).zfill(3)}\n**Audio Title :** `{v_name}.mp3`\n<blockquote><b>𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}\n𝐓𝐨𝐩𝐢𝐜 𝐍𝐚𝐦𝐞 : {t_name}</b></blockquote>\n\n**𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤**{CR}\n'
                        elif caption == "/cc2":
                            cc = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<blockquote><b>⋅ ─  {t_name}  ─ ⋅</b></blockquote>\n\n<b>🎞️ 𝐓𝐢𝐭𝐥𝐞 :</b> {v_name}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} @MR_Toxic_1.mkv</b>\n<b>├── Resolution : [{res}]</b>\n<blockquote><b>📚 Course : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                            cc1 = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<blockquote><b>⋅ ─  {t_name}  ─ ⋅</b></blockquote>\n\n<b>📁 𝐓𝐢𝐭𝐥𝐞 :</b> {v_name}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} @MR_Toxic_1.pdf</b>\n<blockquote><b>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                            cczip = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<blockquote><b>⋅ ─  {t_name}  ─ ⋅</b></blockquote>\n\n<b>📒 𝐓𝐢𝐭𝐥𝐞 :</b> {v_name}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} .zip</b>\n<blockquote><b>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                            ccimg = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<blockquote><b>⋅ ─  {t_name}  ─ ⋅</b></blockquote>\n\n<b>🖼️ 𝐓𝐢𝐭𝐥𝐞 :</b> {v_name}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} .jpg</b>\n<blockquote><b>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                            ccm = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<blockquote><b>⋅ ─  {t_name}  ─ ⋅</b></blockquote>\n\n<b>🎵 𝐓𝐢𝐭𝐥𝐞 :</b> {v_name}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} .mp3</b>\n<blockquote><b>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                            cchtml = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<blockquote><b>⋅ ─  {t_name}  ─ ⋅</b></blockquote>\n\n<b>🌐 𝐓𝐢𝐭𝐥𝐞 :</b> {v_name}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} .html</b>\n<blockquote><b>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                        else:
                            cc = f'<blockquote><b>⋅ ─ {t_name} ─ ⋅</b></blockquote>\n<b>{str(count).zfill(3)}.</b> {v_name} [{res}p] @MR_Toxic_1.mkv'
                            cc1 = f'<blockquote><b>⋅ ─ {t_name} ─ ⋅</b></blockquote>\n<b>{str(count).zfill(3)}.</b> {v_name} @MR_Toxic_1.pdf'
                            cczip = f'<blockquote><b>⋅ ─ {t_name} ─ ⋅</b></blockquote>\n<b>{str(count).zfill(3)}.</b> {v_name} .zip'
                            ccimg = f'<blockquote><b>⋅ ─ {t_name} ─ ⋅</b></blockquote>\n<b>{str(count).zfill(3)}.</b> {v_name} .jpg'
                            ccm = f'<blockquote><b>⋅ ─ {t_name} ─ ⋅</b></blockquote>\n<b>{str(count).zfill(3)}.</b> {v_name} .mp3'
                            cchtml = f'<blockquote><b>⋅ ─ {t_name} ─ ⋅</b></blockquote>\n<b>{str(count).zfill(3)}.</b> {v_name} .html'
                    else:
                        if caption == "/cc1":
                            cc = f'**📹 𝐕𝐈𝐃_𝐈𝐃 : {str(count).zfill(3)}.\n\n📝𝐓𝐢𝐭𝐥𝐞 :{name1} [{res}p] @MR_Toxic_1.mkv\n\n<pre><code>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</code></pre>\n\n📥 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}\n\n**➽━━━⊱∘₊𝙏𝙚𝙖𝙢★𝙏𝙤𝙭𝙞𝙘₊∘⊰━━━❥**'
                            cc1 = f'**💾𝐏𝐃𝐅_𝐈𝐃 : {str(count).zfill(3)}.\n\n📝𝐓𝐢𝐭𝐥𝐞 :{name1} @MR_Toxic_1.pdf\n\n<pre><code>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</code></pre>\n\n📥 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}\n\n**➽━━━⊱∘₊𝙏𝙚𝙖𝙢★𝙏𝙤𝙭𝙞𝙘₊∘⊰━━━❥**'
                            cczip = f'[📁]Zip Id : {str(count).zfill(3)}\n**Zip Title :** `{name1}.zip`\n<blockquote><b>Batch Name :</b> {b_name}</blockquote>\n\n**𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤**{CR}\n' 
                            ccimg = f'[🖼️]Img Id : {str(count).zfill(3)}\n**Img Title :** `{name1}.jpg`\n<blockquote><b>Batch Name :</b> {b_name}</blockquote>\n\n**𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤**{CR}\n'
                            ccm = f'[🎵]Audio Id : {str(count).zfill(3)}\n**Audio Title :** `{name1}.mp3`\n<blockquote><b>Batch Name :</b> {b_name}</blockquote>\n\n**𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤**{CR}\n'
                            cchtml = f'[🌐]Html Id : {str(count).zfill(3)}\n**Html Title :** `{name1}.html`\n<blockquote><b>Batch Name :</b> {b_name}</blockquote>\n\n**𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤**{CR}\n'
                        elif caption == "/cc2":
                            cc = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<b>🎞️ 𝐓𝐢𝐭𝐥𝐞 :</b> {name1}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} @MR_Toxic_1.mkv</b>\n<b>├── Resolution : [{res}]</b>\n<blockquote><b>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                            cc1 = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<b>📁 𝐓𝐢𝐭𝐥𝐞 :</b> {name1}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} @MR_Toxic_1.pdf</b>\n<blockquote><b>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                            cczip = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<b>📒 𝐓𝐢𝐭𝐥𝐞 :</b> {name1}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} .zip</b>\n<blockquote><b>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                            ccimg = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<b>🖼️ 𝐓𝐢𝐭𝐥𝐞 :</b> {name1}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} .jpg</b>\n<blockquote><b>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                            ccm = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<b>🎵 𝐓𝐢𝐭𝐥𝐞 :</b> {name1}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} .mp3</b>\n<blockquote><b>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                            cchtml = f"——— ✦ {str(count).zfill(3)} ✦ ———\n\n<b>🌐 𝐓𝐢𝐭𝐥𝐞 :</b> {name1}\n<b>├── 𝐄𝐱𝐭𝐞𝐧𝐭𝐢𝐨𝐧 :  {CR} .html</b>\n<blockquote><b>📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 : {b_name}</b></blockquote>\n\n**🌟 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲⬩➤ : {CR}**"
                        else:
                            cc = f'<b>{str(count).zfill(3)}.</b> {name1} [{res}p] @MR_Toxic_1.mkv'
                            cc1 = f'<b>{str(count).zfill(3)}.</b> {name1} @MR_Toxic_1.pdf'
                            cczip = f'<b>{str(count).zfill(3)}.</b> {name1} .zip'
                            ccimg = f'<b>{str(count).zfill(3)}.</b> {name1} .jpg'
                            ccm = f'<b>{str(count).zfill(3)}.</b> {name1} .mp3'
                            cchtml = f'<b>{str(count).zfill(3)}.</b> {name1} .html'
#........................................................................................................................................................................................
                remaining_links = len(links) - count
                progress = (count / len(links)) * 100
                Show = f"<i><b>Video Downloading</b></i>\n<blockquote><b>{str(count).zfill(3)}) {name1}</b></blockquote>" 
                Show1 = f"<blockquote>🚀𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬 » {progress:.2f}%</blockquote>\n┃\n" \
                        f"┣🔗𝐈𝐧𝐝𝐞𝐱 » {count}/{len(links)}\n┃\n" \
                        f"╰━🖇️𝐑𝐞𝐦𝐚𝐢𝐧 » {remaining_links}\n" \
                        f"━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                        f"<blockquote><b>⚡Dᴏᴡɴʟᴏᴀᴅɪɴɢ Sᴛᴀʀᴛᴇᴅ...⏳</b></blockquote>\n┃\n" \
                        f'┣💃𝐂𝐫𝐞𝐝𝐢𝐭 » {CR}\n┃\n' \
                        f"╰━📚𝐁𝐚𝐭𝐜𝐡 » {b_name}\n" \
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                        f"<blockquote>📚𝐓𝐢𝐭𝐥𝐞 » {namef}</blockquote>\n┃\n" \
                        f"┣🍁𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {quality}\n┃\n" \
                        f'┣━🔗𝐋𝐢𝐧𝐤 » <a href="{link0}">**Original Link**</a>\n┃\n' \
                        f'╰━━🖇️𝐔𝐫𝐥 » <a href="{url}">**Api Link**</a>\n' \
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
                        f"🛑**Send** /stop **to stop process**\n┃\n" \
                        f"╰━✦𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐁𝐲 ✦ {CREDIT}💥."
#........................................................................................................................................................................................           
                if "drive" in url:
                    try:
                        ka = await helper.download(url, namef)
                        await helper.send_doc(bot, m, None, ka, cc1, None, count, name, channel_id, pdfwatermark, pdfthumb)
                        count+=1
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    
  
                elif "pdf" in url:
                    if "cwmediabkt99" in url:
                        max_retries = 15  # Define the maximum number of retries
                        retry_delay = 4  # Delay between retries in seconds
                        success = False  # To track whether the download was successful
                        failure_msgs = []  # To keep track of failure messages
                        
                        for attempt in range(max_retries):
                            try:
                                await asyncio.sleep(retry_delay)
                                url = url.replace(" ", "%20")
                                scraper = cloudscraper.create_scraper()
                                response = scraper.get(url)

                                if response.status_code == 200:
                                    with open(f'{namef}.pdf', 'wb') as file:
                                        file.write(response.content)
                                    await asyncio.sleep(retry_delay)  # Optional, to prevent spamming
                                    await helper.send_doc(bot, m, None, f'{namef}.pdf', cc1, None, count, name, channel_id, pdfwatermark, pdfthumb)
                                    count += 1
                                    success = True
                                    break  # Exit the retry loop if successful
                                else:
                                    failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {response.status_code} {response.reason}")
                                    failure_msgs.append(failure_msg)
                                    
                            except Exception as e:
                                failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                                failure_msgs.append(failure_msg)
                                await asyncio.sleep(retry_delay)
                                continue 
                        for msg in failure_msgs:
                            await msg.delete()
                            
                    else:
                        try:
                            cmd = f'yt-dlp -o "{namef}.pdf" "{url}" -R 25 --fragment-retries 25'
                            result = subprocess.run(cmd, shell=True, timeout=300)
                            if os.path.exists(f'{namef}.pdf'):
                                await helper.send_doc(bot, m, None, f'{namef}.pdf', cc1, None, count, name, channel_id, pdfwatermark, pdfthumb)
                            else:
                                await bot.send_message(channel_id, f"⚠️ PDF download failed: `{name}`")
                            count += 1
                        except subprocess.TimeoutExpired:
                            await bot.send_message(channel_id, f"⏰ PDF download timed out: `{name}`")
                            count += 1
                            failed_count += 1
                            continue
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue
           
                elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{namef}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_photo(chat_id=channel_id, photo=f'{namef}.{ext}', caption=ccimg)
                        count += 1
                        os.remove(f'{namef}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    

                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{namef}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=channel_id, document=f'{namef}.{ext}', caption=ccm)
                        count += 1
                        os.remove(f'{namef}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue    
                    
                elif 'encrypted.m' in url:    
                    prog = await bot.send_message(channel_id, Show, disable_web_page_preview=True)
                    prog1 = await m.reply_text(Show1, disable_web_page_preview=True)
                    res_file = await helper.download_and_decrypt_video(url, cmd, namef, appxkey)  
                    filename = res_file  
                    await prog1.delete(True)
                    await helper.send_vid(bot, m, cc, filename, vidwatermark, thumb, name, prog, channel_id)
                    count += 1  
                    await asyncio.sleep(1)  
                    continue  

                elif 'drmcdni' in url or 'drm/wv' in url or 'drm/common' in url:
                    prog = await bot.send_message(channel_id, Show, disable_web_page_preview=True)
                    prog1 = await m.reply_text(Show1, disable_web_page_preview=True)
                    res_file = await helper.decrypt_and_merge_video(mpd, keys_string, path, namef, raw_text2)
                    filename = res_file
                    await prog1.delete(True)
                    await helper.send_vid(bot, m, cc, filename, vidwatermark, thumb, name, prog, channel_id)
                    count += 1
                    await asyncio.sleep(1)
                    continue
     
                else:
                    prog = await bot.send_message(channel_id, Show, disable_web_page_preview=True)
                    prog1 = await m.reply_text(Show1, disable_web_page_preview=True)
                    res_file = await helper.download_video(url, cmd, namef)
                    filename = res_file
                    await prog1.delete(True)
                    await helper.send_vid(bot, m, cc, filename, vidwatermark, thumb, name, prog, channel_id)
                    count += 1
                    time.sleep(1)
                
            except Exception as e:
                await bot.send_message(channel_id, f'⚠️**𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐅𝐚𝐢𝐥𝐞𝐝**⚠️\n**𝐍𝐚𝐦𝐞** =>> `{str(count).zfill(3)} {name1}`\n**𝐔𝐑𝐋** =>> {url}\n\n<blockquote expandable><i><b>𝐅𝐚𝐢𝐥𝐞𝐝 𝐑𝐞𝐚𝐬𝐨𝐧: {str(e)}</b></i></blockquote>', disable_web_page_preview=True)
                count += 1
                failed_count += 1
                continue

    except Exception as e:
        await m.reply_text(e)
        time.sleep(2)

    success_count = len(links) - int(raw_text) - failed_count + 1
    video_count = len(links) - pdf_count - img_count
    if m.document:
        await bot.send_message(channel_id, f"<blockquote>🔗 𝐓𝐨𝐭𝐚𝐥 𝐔𝐑𝐋𝐬 URLs: {len(links)} \n┠🔴 𝐓𝐨𝐭𝐚𝐥 𝐅𝐚𝐢𝐥𝐞𝐝 𝐔𝐑𝐋𝐬: {failed_count}\n┠🟢 𝐓𝐨𝐭𝐚𝐥 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥 𝐔𝐑𝐋𝐬: {success_count}\n┃   ┠🎥 𝐓𝐨𝐭𝐚𝐥 𝐕𝐢𝐝𝐞𝐨 𝐔𝐑𝐋𝐬: {video_count}\n┃   ┠📄 𝐓𝐨𝐭𝐚𝐥 𝐏𝐃𝐅 𝐔𝐑𝐋𝐬: {pdf_count}\n┃   ┠📸 𝐓𝐨𝐭𝐚𝐥 𝐈𝐌𝐀𝐆𝐄 𝐔𝐑𝐋𝐬: {img_count}</blockquote>\n**➽━━━⊱∘₊𝙏𝙚𝙖𝙢★𝙏𝙤𝙭𝙞𝙘₊∘⊰━━━❥**\n")
        await bot.send_message(channel_id, f"⋅ ─ 𝐥𝐢𝐬𝐭 𝐢𝐧𝐝𝐞𝐱 ({raw_text}-{len(links)}) 𝐨𝐮𝐭 𝐨𝐟 𝐫𝐚𝐧𝐠𝐞 ─ ⋅\n<blockquote><b>📚Batch : {b_name}</b></blockquote>\n⋅ ─ ✅DOWNLOADING ✩ COMPLETED ─ ⋅")
        if "/Baby" not in raw_text7:
            await bot.send_message(m.chat.id, f"<blockquote><b>💕𝐘𝐨𝐮𝐫 𝐓𝐚𝐬𝐤 𝐢𝐬 𝐜𝐨𝐦𝐩𝐥𝐞𝐭𝐞𝐝,𝐩𝐥𝐞𝐚𝐬𝐞 𝐜𝐡𝐞𝐜𝐤 𝐲𝐨𝐮𝐫 𝐒𝐞𝐭 𝐂𝐡𝐚𝐧𝐧𝐞𝐥📱.</b></blockquote>")

#============================================================================================================
# ── Simple in-memory user store ──────────────────────────────────────────────
_user_ids: set = set()

class db:
    @staticmethod
    def register_user(user_id: int):
        _user_ids.add(user_id)

    @staticmethod
    def get_all_user_ids():
        return list(_user_ids)
# ─────────────────────────────────────────────────────────────────────────────

# ── /owner command ─────────────────────────────────────────────────────────────
def register_owner_commands(bot):
    @bot.on_message(filters.command("owner") & filters.private)
    async def owner_handler(client: Client, msg: Message):
        db.register_user(msg.from_user.id)
        owner_text = (
            "┌──────────────────────────┐\n"
            "**💥Contact**: @CinderellaContactBot\n"
            "└──────────────────────────┘\n\n"
        )
        await msg.reply_text(owner_text)


    # ── /changeapi command (owner only) ───────────────────────────────────────
    # Usage: /changeapi https://new-api.example.com/pw
    # Updates both PWAPI1 and PWAPI2 at once (they always use the same API)
    @bot.on_message(filters.command("changeapi") & filters.private)
    async def changeapi_handler(client: Client, msg: Message):
        global PWAPI1, PWAPI2
        if msg.from_user.id != OWNER:
            return await msg.reply_text(
                "To change your Api in your Repository in this format👇🏻.\n\n"
                "/changeapi New Api Here\n**https... to .com/pw** tak Only😁.\n\n"
                "But But But🫡\n"
                "Sorry you are not my owner😒."
            )

        parts = msg.text.split(None, 1)
        if len(parts) < 2 or not parts[1].strip():
            return await msg.reply_text(
                "Welcome Boss To change your Api in your Repository in this format\n\n"
                "/changeapi New Api Here\n**https... to .com/pw** tak Only😁.\n\n"
                "Send me I will change it.✨"
            )

        new_api = parts[1].strip()
        PWAPI1 = new_api
        PWAPI2 = new_api
        await msg.reply_text(
            f" **💕𝐀𝐩𝐢 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐂𝐡𝐚𝐧𝐠𝐞𝐝!**\n\n"
            f"🔗 **𝐍𝐞𝐰 𝐀𝐩𝐢:**\n`{PWAPI1}`\n\n"
            f"⚡ 𝐂𝐡𝐚𝐧𝐠𝐞𝐝 𝐋𝐢𝐯𝐞 𝐍𝐨𝐰 — 𝐍𝐨 𝐁𝐨𝐭 𝐫𝐞𝐬𝐭𝐚𝐫𝐭 𝐧𝐞𝐞𝐝𝐞𝐝 𝐔𝐬𝐞 𝐍𝐨𝐰🚀."
        )

#============================================================================================================
# ── /download eligibility store ──────────────────────────────────────────────
# chat_id → True means user has used /download and is eligible to send txt/link
_download_eligible: dict = {}

#============================================================================================================
def register_drm_handlers(bot):
    register_owner_commands(bot)

    # ── /download command ─────────────────────────────────────────────────────
    @bot.on_message(filters.command("download") & filters.private)
    async def download_command_handler(client: Client, m: Message):
        _download_eligible[m.chat.id] = True
        await m.reply_text(
            " **💕𝐒𝐮𝐩𝐩𝐞𝐫𝐛 𝐍𝐨𝐰 𝐲𝐨𝐮 𝐚𝐫𝐞 𝐄𝐥𝐢𝐠𝐢𝐛𝐥𝐞 𝐭𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐯𝐢𝐝𝐞𝐨𝐬 & 𝐩𝐝𝐟.**\n\n"
            "📁**𝐒𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 𝐭𝐱𝐭 𝐟𝐢𝐥𝐞 𝐨𝐫 𝐝𝐢𝐫𝐞𝐜𝐭 𝐥𝐢𝐧𝐤 𝐭𝐨 𝐬𝐭𝐚𝐫𝐭 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠.**"
        )

    # ── main drm handler ─────────────────────────────────────────────────────
    @bot.on_message(filters.private & (filters.document | filters.text))
    async def call_drm_handler(bot: Client, m: Message):
        # Skip all bot commands — also revokes /download eligibility for any other command
        if m.text and m.text.startswith("/"):
            if not m.text.startswith("/download"):
                # Any other command cancels eligibility
                _download_eligible.pop(m.chat.id, None)
            return
        # Skip non-.txt documents (e.g. PDF sent by user in pdfrename flow)
        if m.document and not m.document.file_name.endswith(".txt"):
            return
        # Block download unless /download was sent first
        if not _download_eligible.get(m.chat.id):
            return
        # Consume eligibility — one-time use, revoked after this
        _download_eligible.pop(m.chat.id, None)
        await drm_handler(bot, m)
