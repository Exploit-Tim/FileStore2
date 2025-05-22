from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db
from bot import Bot

@Bot.on_message(filters.command("settings"))
async def settings_command(client: Client, message: Message):
    keyboard = [
        [InlineKeyboardButton("ᴀᴅᴍɪɴ", callback_data="daftar_admin")],
        [
            InlineKeyboardButton("ғsᴜʙ", callback_data="daftar_fsub"),
            InlineKeyboardButton("ᴍᴏᴅᴇ", callback_data="Mode_fsub"),
        ],
        [
            InlineKeyboardButton("ᴅʙ ɪᴅ", callback_data="db_id"),
            InlineKeyboardButton("ᴅʙ ᴜʀʟ", callback_data="db_url"),
        ],
        [InlineKeyboardButton("ᴘʀᴏᴛᴇᴄᴛ", callback_data="protect")],
        [
            InlineKeyboardButton("ᴛɪᴍᴇ", callback_data="time_delete"),
            InlineKeyboardButton("sᴇʀᴠᴇʀ", callback_data="server_info"),
        ],
        [
            InlineKeyboardButton("ᴍᴇssᴀɢᴇ", callback_data="set_force_msg"),
            InlineKeyboardButton("ᴘɪᴄᴛ", callback_data="set_welcome"),
        ],
        [InlineKeyboardButton("ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ", callback_data="custom_caption")],
        [InlineKeyboardButton("ᴋᴏɴᴛᴇɴ", callback_data="konten")],
        [InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="close")],
    ]
    await message.reply_text("📋 <b>Menu Settings</b>", reply_markup=InlineKeyboardMarkup(keyboard))
