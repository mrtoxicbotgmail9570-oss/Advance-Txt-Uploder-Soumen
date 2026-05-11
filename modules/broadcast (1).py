import os
import asyncio
import requests
import subprocess
from vars import OWNER, CREDIT, AUTH_USERS, TOTAL_USERS
from pyrogram import Client, filters
from pyrogram.types import Message

def register_broadcast_handlers(bot):
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_message(filters.command("broadcast") & filters.private)
    async def broadcast_handler(client: Client, message: Message):
        if message.chat.id != OWNER:
            return

        if not message.reply_to_message:
            return await message.reply_text(
                "📢 **Broadcast Mode**\n\n"
                "please Boss reply with such a content for broadcasting."
            )

        content = message.reply_to_message
        all_users = list(set(TOTAL_USERS))

        if not all_users:
            return await message.reply_text("❌ No users in database yet.")

        sent = 0
        failed = 0
        status_msg = await message.reply_text(f"📤 Broadcasting to `{len(all_users)}` users...")

        for user_id in all_users:
            try:
                await content.copy(user_id)
                sent += 1
            except Exception:
                failed += 1
            await asyncio.sleep(0.05)  # small delay to avoid flood

        await status_msg.edit_text(
            f"✅ **Broadcast Complete!**\n\n"
            f"📨 Sent: `{sent}`\n"
            f"❌ Failed: `{failed}`\n"
            f"👥 Total: `{len(all_users)}`"
        )
  
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_message(filters.command("broadusers") & filters.private)
    async def broadusers_handler(client: Client, message: Message):
        if message.chat.id != OWNER:
            return

        if not TOTAL_USERS:
            await message.reply_text("**No Broadcasted User**")
            return

        user_infos = []
        for user_id in list(set(TOTAL_USERS)):
            try:
                user = await client.get_users(int(user_id))
                fname = user.first_name if user.first_name else " "
                user_infos.append(f"[{user.id}](tg://openmessage?user_id={user.id}) | `{fname}`")
            except Exception:
                user_infos.append(f"`{user_id}`")

        total = len(user_infos)
        header = (
            f"<blockquote><b>Total Users: {total}</b></blockquote>\n\n"
            "<b>Users List:</b>\n"
        )

        chunk = header
        for line in user_infos:
            if len(chunk) + len(line) + 1 > 4096:
                await message.reply_text(chunk, parse_mode=ParseMode.HTML)
                chunk = ""
            chunk += line + "\n"
        if chunk:
            await message.reply_text(chunk, parse_mode=ParseMode.HTML)

# .....,.....,.......,...,.......,.....,...,.......,...,.......,.....,
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
