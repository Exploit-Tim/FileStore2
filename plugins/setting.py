from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db
from bot import Bot

@Bot.on_message(filters.command("settings"))
async def settings_command(client: Client, message: Message):
    keyboard = [
        [InlineKeyboardButton("𝗔𝗗𝗠𝗜𝗡", callback_data="daftar_admin")],
        [
            InlineKeyboardButton("𝗙𝗦𝗨𝗕", callback_data="daftar_fsub"),
            InlineKeyboardButton("𝗠𝗢𝗗𝗘", callback_data="Mode_fsub"),
        ],
        [
            InlineKeyboardButton("𝗗𝗕 𝗜𝗗", callback_data="db_id"),
            InlineKeyboardButton("𝗗𝗕 𝗨𝗥𝗟", callback_data="db_url"),
        ],
        [InlineKeyboardButton("𝗣𝗥𝗢𝗧𝗘𝗖𝗧", callback_data="protect")],
        [
            InlineKeyboardButton("𝗧𝗜𝗠𝗘", callback_data="time_delete"),
            InlineKeyboardButton("𝗦𝗘𝗥𝗩𝗘𝗥", callback_data="server_info"),
        ],
        [
            InlineKeyboardButton("𝗠𝗘𝗦𝗦𝗔𝗚𝗘", callback_data="set_force_msg"),
            InlineKeyboardButton("𝗣𝗜𝗖𝗧", callback_data="menu_pict"),
        ],
        [InlineKeyboardButton("𝗖𝗨𝗦𝗧𝗢𝗠 𝗖𝗔𝗣𝗧𝗜𝗢𝗡", callback_data="custom_caption")],
        [InlineKeyboardButton("𝗞𝗢𝗡𝗧𝗘𝗡", callback_data="konten")],
        [InlineKeyboardButton("𝗧𝗨𝗧𝗨𝗣", callback_data="close")],
    ]
    await message.reply_text("<b>𝗠𝗲𝗻𝘂 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀</b>", reply_markup=InlineKeyboardMarkup(keyboard))
