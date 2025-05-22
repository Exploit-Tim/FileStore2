from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot import Bot
from database.database import db

@Bot.on_message(filters.command('settings'))
async def setting_menu(client, message: Message):
    keyboard = [
        [InlineKeyboardButton("Daftar Admin", callback_data="daftar_admin")],
        [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
        [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
        [InlineKeyboardButton("Tutup", callback_data="close")],
    ]
    await message.reply_text(
        "Menu Setting",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@Bot.on_callback_query(filters.regex("daftar_admin"))
async def daftar_admin(client, callback_query: CallbackQuery):
    admin_ids = await db.get_all_admins()
    if not admin_ids:
        admin_list = "<b><blockquote>❌ No admins found.</blockquote></b>"
    else:
        admin_list = "\n".join(f"<b><blockquote>ID: <code>{id}</code></blockquote></b>" for id in admin_ids)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Kembali", callback_data="back_to_settings")]])
    await callback_query.message.edit_text(f"<b>⚡ Current Admin List:</b>\n\n{admin_list}", reply_markup=reply_markup)

@Bot.on_callback_query(filters.regex("back_to_settings"))
async def back_to_settings(client, callback_query: CallbackQuery):
    keyboard = [
        [InlineKeyboardButton("Daftar Admin", callback_data="daftar_admin")],
        [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
        [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
        [InlineKeyboardButton("Tutup", callback_data="close")],
    ]
    await callback_query.message.edit_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))

@Bot.on_callback_query(filters.regex("set_welcome"))
async def set_welcome(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text("Fitur Set Welcome")
    await callback_query.answer("Set Welcome")

@Bot.on_callback_query(filters.regex("set_force_msg"))
async def set_force_msg(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text("Fitur Set Force Message")
    await callback_query.answer("Set Force Message")

@Bot.on_callback_query(filters.regex("close"))
async def close(client, callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer("Menu Ditutup")
