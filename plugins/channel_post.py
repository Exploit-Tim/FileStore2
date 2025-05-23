# (©)Codexbotz
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from helper_func import encode, admin
from pyrogram.enums import ParseMode, ChatAction, ChatMemberStatus, ChatType
from database.database import *


@Bot.on_message(filters.private & admin & ~filters.command([
    'start', 'commands', 'users', 'settings', 'broadcast', 'batch', 'custom_batch',
    'genlink', 'stats', 'dlt_time', 'check_dlt_time', 'dbroadcast', 'ban',
    'unban', 'banlist', 'addchnl', 'delchnl', 'listchnl', 'fsub_mode', 'pbroadcast',
    'add_admin', 'deladmin', 'admins']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Tunggu...", quote=True)

    # Ambil konten channel ID dari database
    KONTEN_CHANNEL_ID = await database.get_konten_channel()

    try:
        post_message = await message.copy(
            chat_id=client.db_channel.id,
            caption="ini caption contoh\n\np",
            disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        post_message = await message.copy(
            chat_id=client.db_channel.id,
            caption="ini caption contoh\n\np",
            disable_notification=True
        )
    except Exception as e:
        print(e)
        await reply_text.edit("❌ Gagal upload ke channel utama.")
        return

    # Encode link
    converted_id = post_message.id * abs(client.db_channel.id)
    base64_string = await encode(f"get-{converted_id}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 Save File", url=link)]
    ])

    konten_status = "❌"
    konten_error = ""

    if KONTEN_CHANNEL_ID:
        try:
            await message.copy(
                chat_id=KONTEN_CHANNEL_ID,
                caption=f"ini caption contoh\n\n{link}",
                reply_markup=reply_markup,
                disable_notification=True
            )
            konten_status = "✅"
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await message.copy(
                    chat_id=KONTEN_CHANNEL_ID,
                    caption=f"ini caption contoh\n\n{link}",
                    reply_markup=reply_markup,
                    disable_notification=True
                )
                konten_status = "✅"
            except Exception as e:
                print(e)
                konten_error = "⚠️ Gagal meneruskan ke channel konten. Periksa ID-nya."
        except Exception as e:
            print(e)
            konten_error = "⚠️ Gagal meneruskan ke channel konten. Periksa ID-nya."

    final_message = f"<b>Here is your link</b>\n\n{link}\n\n📤 Teruskan ke Channel Konten: {konten_status}"
    if konten_error:
        final_message += f"\n{konten_error}"

    await reply_text.edit(
        final_message,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
