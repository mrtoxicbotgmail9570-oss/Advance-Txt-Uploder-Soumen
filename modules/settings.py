import globals
from vars import CREDIT
import random
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InputMediaPhoto

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
def register_settings_handlers(bot):
    
    @bot.on_callback_query(filters.regex("setttings"))
    async def settings_button(client, callback_query):
        caption = "✨ <b>My Premium BOT Settings Panel</b> ✨"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Caption Style", callback_data="caption_style_command"), InlineKeyboardButton("🖋️ File Name", callback_data="file_name_command")],
            [InlineKeyboardButton("🌅 Thumbnail", callback_data="thummbnail_command")],
            [InlineKeyboardButton("✍️ Add Credit", callback_data="add_credit_command"), InlineKeyboardButton("🔏 Set Token", callback_data="set_token_command")],
            [InlineKeyboardButton("💧 Watermark", callback_data="wattermark_command")],
            [InlineKeyboardButton("📽️ Video Quality", callback_data="quality_command"), InlineKeyboardButton("🏷️ Topic", callback_data="topic_command")],
            [InlineKeyboardButton("🔄 Reset", callback_data="resset_command")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
        ])
        await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/45f48779e0aa39709d1e8-4c024567d60f6ec5c2.jpg",
          caption=caption
        ),
        reply_markup=keyboard
        )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("thummbnail_command"))
    async def cmd(client, callback_query):
        user_id = callback_query.from_user.id
        first_name = callback_query.from_user.first_name
        caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to set Thumbnail**"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎥 Video", callback_data="viideo_thumbnail_command"), InlineKeyboardButton("📑 PDF", callback_data="pddf_thumbnail_command")],
            [InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]
        ])
        await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/b23084c3e9124e14e18ec-d385f8f9c8b1635a2e.jpg",
          caption=caption
        ),
        reply_markup=keyboard
        )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("wattermark_command"))
    async def cmd(client, callback_query):
        user_id = callback_query.from_user.id
        first_name = callback_query.from_user.first_name
        caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to set Watermark**"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎥 Video", callback_data="video_wateermark_command"), InlineKeyboardButton("📑 PDF", callback_data="pdf_wateermark_command")],
            [InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]
        ])
        await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/033121ad32291bcaddd01-d91ae4a1f7ca9378fc.jpg",
          caption=caption
        ),
        reply_markup=keyboard
        )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("set_token_command"))
    async def cmd(client, callback_query):
        user_id = callback_query.from_user.id
        first_name = callback_query.from_user.first_name
        caption = f"✨ **Welcome [{first_name}](tg://user?id={user_id})\nChoose Button to set Token**"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Classplus", callback_data="cp_token_command")],
            [InlineKeyboardButton("Physics Wallah", callback_data="pw_token_command"), InlineKeyboardButton("Carrerwill", callback_data="cw_token_command")],
            [InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]
        ])
        await callback_query.message.edit_media(
        InputMediaPhoto(
          media="https://graph.org/file/417cc7326cab9036c0152-f6a281db2a6975dfa9.jpg",
          caption=caption
        ),
        reply_markup=keyboard
        )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("caption_style_command"))
    async def handle_caption(client, callback_query):
        user_id = callback_query.from_user.id
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
        editable = await callback_query.message.edit(
            "**Caption Style 1**\n"
            "<blockquote expandable><b>[🎥]Vid Id</b> : {str(count).zfill(3)}\n"
            "**Video Title :** `{name1} [{res}p].{ext}`\n"
            "<blockquote><b>Batch Name :</b> {b_name}</blockquote>\n\n"
            "**Extracted by➤**{CR}</blockquote>\n\n"
            "**Caption Style 2**\n"
            "<blockquote expandable>**——— ✦ {str(count).zfill(3)} ✦ ———**\n\n"
            "🎞️ **Title** : `{name1}`\n"
            "**├── Extention :  {extension}.{ext}**\n"
            "**├── Resolution : [{res}]**\n"
            "📚 **Course : {b_name}**\n\n"
            "🌟 **Extracted By : {credit}**</blockquote>\n\n"
            "**Caption Style 3**\n"
            "<blockquote expandable>**{str(count).zfill(3)}.** {name1} [{res}p].{ext}</blockquote>\n\n"
            "**Send Your Caption Style eg. /cc1 or /cc2 or /cc3**", reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/cc1":
                globals.caption = '/cc1'
                await editable.edit(f"✅ Caption Style 1 Updated!", reply_markup=keyboard)
            elif input_msg.text.lower() == "/cc2":
                globals.caption = '/cc2'
                await editable.edit(f"✅ Caption Style 2 Updated!", reply_markup=keyboard)
            else:
                globals.caption = input_msg.text
                await editable.edit(f"✅ Caption Style 3 Updated!", reply_markup=keyboard)
            
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Caption Style:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("file_name_command"))
    async def handle_caption(client, callback_query):
        user_id = callback_query.from_user.id
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
        editable = await callback_query.message.edit("**Send End File Name or Send /d**", reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/d":
                globals.endfilename = '/d'
                await editable.edit(f"✅ End File Name Disabled !", reply_markup=keyboard)
            else:
                globals.endfilename = input_msg.text
                await editable.edit(f"✅ End File Name `{globals.endfilename}` is enabled!", reply_markup=keyboard)            
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set End File Name:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("viideo_thumbnail_command"))
    async def video_thumbnail(client, callback_query):
        user_id = callback_query.from_user.id
        first_name = callback_query.from_user.first_name
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🟢 Set Video Cover", callback_data="set_video_cover_command")],
            [InlineKeyboardButton("👁️ View Video Cover", callback_data="view_video_cover_command")],
            [InlineKeyboardButton("❌ Delete Video Cover", callback_data="del_video_cover_command")],
            [InlineKeyboardButton("🔙 Back to Thumbnail", callback_data="thummbnail_command")]
        ])
        await callback_query.message.edit(
            f"**🎥 Video Cover Settings**\n\n"
            f"**Welcome [{first_name}](tg://user?id={user_id})**\n\n"
            f"**😍You can Change Video Cover Photo Also tap on /changecover to do this.\n\n"
            f"<blockquote>Video Cover globally set hoga jo /renamevideo aur /setvideocover commands mein use hoga.\n"
            f"Sirf Telegram direct photo supported hai.</blockquote>",
            reply_markup=keyboard
        )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("set_video_cover_command"))
    async def set_video_cover_settings(client, callback_query):
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Video Cover", callback_data="viideo_thumbnail_command")]])
        editable = await callback_query.message.edit(
            "**🖼️ Video Cover Set**\n\n"
            "📸 **Direct Telegram se photo bhejo** as Global Video Cover.\n\n"
            "<blockquote>⚠️ Note: Sirf Telegram photo supported hai. URL supported nahi hai.\n"
            "Send /d to disable cover.</blockquote>",
            reply_markup=keyboard
        )
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text and input_msg.text.strip().lower() == "/d":
                globals.videocover = "/d"
                from video_cover import delete_videocover_for_user
                delete_videocover_for_user(callback_query.from_user.id)
                await editable.edit("✅ **Video Cover Disabled!**", reply_markup=keyboard)
            elif input_msg.photo:
                file_id = input_msg.photo.file_id
                globals.videocover = file_id
                from video_cover import save_videocover_for_user
                save_videocover_for_user(callback_query.from_user.id, file_id)
                await editable.edit("✅ **Video Cover set from photo!**\n<blockquote>Ye cover ab videos mein use hoga.</blockquote>", reply_markup=keyboard)
            else:
                await editable.edit("❌ Invalid input! Sirf Telegram photo bhejein.", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("view_video_cover_command"))
    async def view_video_cover_settings(client, callback_query):
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Video Cover", callback_data="viideo_thumbnail_command")]])
        from video_cover import get_videocover_for_user
        saved = get_videocover_for_user(callback_query.from_user.id)
        if saved == "/d" or not saved:
            await callback_query.message.edit("📭 **Video Cover set nahi hai.**\n\nUse /setvideocover to set one.", reply_markup=keyboard)
            return
        try:
            await callback_query.message.reply_photo(
                photo=saved,
                caption="🎥 **Your Current Video Cover**\n<blockquote>Status: ✅ Active</blockquote>"
            )
            await callback_query.message.edit("✅ Cover shown above.", reply_markup=keyboard)
        except Exception as e:
            await callback_query.message.edit(f"🎥 Video Cover set hai.\n⚠️ Preview error: {str(e)[:100]}", reply_markup=keyboard)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("del_video_cover_command"))
    async def del_video_cover_settings(client, callback_query):
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Video Cover", callback_data="viideo_thumbnail_command")]])
        from video_cover import get_videocover_for_user, delete_videocover_for_user
        saved = get_videocover_for_user(callback_query.from_user.id)
        if saved == "/d" or not saved:
            await callback_query.message.edit("📭 **Koi Video Cover set nahi hai.**", reply_markup=keyboard)
            return
        globals.videocover = "/d"
        delete_videocover_for_user(callback_query.from_user.id)
        await callback_query.message.edit("❌ **Video Cover deleted!**\n\nUse /setvideocover to set a new one.", reply_markup=keyboard)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("pddf_thumbnail_command"))
    async def pdf_thumbnail_button(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💥𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐑𝐞𝐜𝐚𝐩𝐭𝐢𝐨𝐧", url="https://t.me/Cinderella_recaptionBot"), InlineKeyboardButton("💥𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐒𝐭𝐫𝐢𝐧𝐠", url="https://t.me/Cinderella_StringBot")],
            [InlineKeyboardButton("🔙 Back to Settings", callback_data="thummbnail_command")]
        ])
        await callback_query.message.edit(
            "**📸 PDF Thumbnail**\n\n"
            "⚠️ **Temporary Unavailable**\n"
            "This feature is not available in this Bot.\n\n"
            "Use Powerful Recaption Bot **@Cinderella_recaptionBot**\n"
            "If you want to Generate your String Session so use **@Cinderella_StringBot**",
            reply_markup=keyboard
        )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("add_credit_command"))
    async def credit(client, callback_query):
        user_id = callback_query.from_user.id
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
        editable = await callback_query.message.edit(f"Send Credit Name or Send /d", reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/d":
                globals.CR = f"{CREDIT}"
                await editable.edit(f"✅ Credit set to default !", reply_markup=keyboard)
            else:
                globals.CR = input_msg.text
                await editable.edit(f"✅ Credit set as {globals.CR} !", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Credit:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("cp_token_command"))
    async def handle_token(client, callback_query):
        user_id = callback_query.from_user.id
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="set_token_command")]])
        editable = await callback_query.message.edit("**Send Classplus Token**", reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            globals.cptoken = input_msg.text
            await editable.edit(f"✅ Classplus Token set successfully !\n\n<blockquote expandable>`{globals.cptoken}`</blockquote>", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Classplus Token:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("pw_token_command"))
    async def handle_token(client, callback_query):
        user_id = callback_query.from_user.id
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="set_token_command")]])
        editable = await callback_query.message.edit("**Send Physics Wallah Same Batch Token**", reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            globals.pwtoken = input_msg.text
            await editable.edit(f"✅ Physics Wallah Token set successfully !\n\n<blockquote expandable>`{globals.pwtoken}`</blockquote>", reply_markup=keyboard) 
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Physics Wallah Token:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("cw_token_command"))
    async def handle_token(client, callback_query):
        user_id = callback_query.from_user.id
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="set_token_command")]])
        editable = await callback_query.message.edit("**Send Carrerwill Token or Send /d for default**", reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/d":
                globals.cwtoken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                await editable.edit(f"✅ Carrerwill Token set successfully as default !", reply_markup=keyboard)
            else:
                globals.cwtoken = input_msg.text
                await editable.edit(f"✅ Carrerwill Token set successfully !\n\n<blockquote expandable>`{globals.cwtoken}`</blockquote>", reply_markup=keyboard)      
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Careerwill Token:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("video_wateermark_command"))
    async def video_watermark(client, callback_query):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💥𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐑𝐞𝐜𝐚𝐩𝐭𝐢𝐨𝐧", url="https://t.me/Cinderella_recaptionBot"), InlineKeyboardButton("💥𝐂𝐢𝐧𝐝𝐞𝐫𝐞𝐥𝐥𝐚 𝐒𝐭𝐫𝐢𝐧𝐠", url="https://t.me/Cinderella_StringBot")],
            [InlineKeyboardButton("🔙 Back to Settings", callback_data="wattermark_command")]
        ])
        await callback_query.message.edit(
            "**🎥 Video Watermark**\n\n"
            "⚠️ **Temporary Unavailable**\n"
            "This feature is not available in this Bot.\n\n"
            "Use Powerful Recaption Bot **@Cinderella_recaptionBot**\n"
            "If you want to Generate your String Session so use **@Cinderella_StringBot**",
            reply_markup=keyboard
        )
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("pdf_wateermark_command"))
    async def pdf_watermark_button(client, callback_query):
        user_id = callback_query.from_user.id
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="wattermark_command")]])
        editable = await callback_query.message.edit(
            f"**Send PDF Watermark text or Send /d to disable**\n"
            f"<blockquote><b>Note:</b> Only text supported (e.g. Sharukh Khan, Munna). "
            f"It will appear at top-right on every PDF page with 30% opacity at 45° angle.</blockquote>",
            reply_markup=keyboard
        )
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/d":
                globals.pdfwatermark = "/d"
                await editable.edit(f"**PDF Watermark Disabled ✅** !", reply_markup=keyboard)
            else:
                globals.pdfwatermark = input_msg.text
                await editable.edit(f"PDF Watermark `{globals.pdfwatermark}` enabled ✅!", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set PDF Watermark:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("quality_command"))
    async def handle_quality(client, callback_query):
        user_id = callback_query.from_user.id
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
        editable = await callback_query.message.edit("__**Enter resolution or Video Quality (`144`, `240`, `360`, `480`, `720`, `1080`) or Send /d**__", reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "144":
                globals.raw_text2 = '144'
                globals.quality = f"{globals.raw_text2}p"
                globals.res = '256x144'
                await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
            elif input_msg.text.lower() == "240":
                globals.raw_text2 = '240'
                globals.quality = f"{globals.raw_text2}p"
                globals.res = '426x240'
                await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
            elif input_msg.text.lower() == "360":
                globals.raw_text2 = '360'
                globals.quality = f"{globals.raw_text2}p"
                globals.res = '640x360'
                await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
            elif input_msg.text.lower() == "480":
                globals.raw_text2 = '480'
                globals.quality = f"{globals.raw_text2}p"
                globals.res = '854x480'
                await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
            elif input_msg.text.lower() == "720":
                globals.raw_text2 = '720'
                globals.quality = f"{globals.raw_text2}p"
                globals.res = '1280x720'
                await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
            elif input_msg.text.lower() == "1080":
                globals.raw_text2 = '1080'
                globals.quality = f"{globals.raw_text2}p"
                globals.res = '1920x1080'
                await editable.edit(f"✅ Video Quality set {globals.quality} !", reply_markup=keyboard)
            else:
                globals.raw_text2 = '480'
                globals.quality = f"{globals.raw_text2}p"
                globals.res = '854x480'
                await editable.edit(f"✅ Video Quality set {globals.quality} as Default !", reply_markup=keyboard)  
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Video Quality:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("topic_command"))
    async def video_watermark(client, callback_query):
        user_id = callback_query.from_user.id
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
        editable = await callback_query.message.edit(f"**If you want to enable topic in caption: send /yes or send /d**\n\n<blockquote><b>Topic fetch from (bracket) in title</b></blockquote>", reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/yes":               
                globals.topic = "/yes"
                await editable.edit(f"**Topic enabled in Caption ✅** !", reply_markup=keyboard)
            else:
                globals.topic = input_msg.text
                await editable.edit(f"Topic disabled in Caption ✅!", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to set Topic in Caption:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)
# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
    @bot.on_callback_query(filters.regex("resset_command"))
    async def credit(client, callback_query):
        user_id = callback_query.from_user.id
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Settings", callback_data="setttings")]])
        editable = await callback_query.message.edit(f"If you want to reset settings send /yes or Send /no", reply_markup=keyboard)
        input_msg = await bot.listen(editable.chat.id)
        try:
            if input_msg.text.lower() == "/yes":
                globals.caption = '/cc1'
                globals.endfilename = '/d'
                globals.thumb = '/d'
                globals.CR = f"{CREDIT}"
                globals.cwtoken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                globals.cptoken = "cptoken"
                globals.pwtoken = "pwtoken"
                globals.vidwatermark = '/d'
                globals.pdfwatermark = '/d'
                globals.videocover = '/d'
                globals.pdfthumb = '/d'
                globals.raw_text2 = '480'
                globals.quality = '480p'
                globals.res = '854x480'
                globals.topic = '/d'
                # ← pdfthumb persistent store bhi clear karo (settings reset = thumb bhi reset)
                _THUMB_STORE = "pdfthumb_store.json"
                import os as _os
                if _os.path.exists(_THUMB_STORE):
                    _os.remove(_THUMB_STORE)
                _VCOVER_STORE = "videocover_store.json"
                if _os.path.exists(_VCOVER_STORE):
                    _os.remove(_VCOVER_STORE)
                await editable.edit(f"✅ Settings reset as default !", reply_markup=keyboard)
            else:
                await editable.edit(f"✅ Settings Not Changed !", reply_markup=keyboard)
        except Exception as e:
            await editable.edit(f"<b>❌ Failed to Change Settings:</b>\n<blockquote expandable>{str(e)}</blockquote>", reply_markup=keyboard)
        finally:
            await input_msg.delete(True)

# .....,.....,.......,...,.......,....., .....,.....,.......,...,.......,.....,
