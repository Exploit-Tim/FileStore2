from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db
from bot import Bot

@Bot.on_message(filters.command("settings"))
async def settings_command(client: Client, message: Message):
    keyboard = [
        [InlineKeyboardButton("Daftar Admin", callback_data="daftar_admin")],
        [InlineKeyboardButton("Daftar Fsub", callback_data="daftar_fsub")],
        [InlineKeyboardButton("Mode Fsub", callback_data="Mode_fsub")],
        [InlineKeyboardButton("Time Delete", callback_data="time_delete")],
        [InlineKeyboardButton("Server Info", callback_data="server_info")],
        [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
        [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
        [InlineKeyboardButton("Tutup", callback_data="close")],
    ]
    await message.reply_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))
