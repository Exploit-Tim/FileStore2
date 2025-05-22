from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import db
from bot import Bot

@Bot.on_message(filters.command("settings"))
async def settings_command(client: Client, message: Message):
    keyboard = [
        [InlineKeyboardButton("Menu Admin", callback_data="menu_admin")],
        [InlineKeyboardButton("Menu Fsub", callback_data="menu_fsub")],
        [InlineKeyboardButton("Menu Fsub Mode", callback_data="menu_fsub_mode")],
        [InlineKeyboardButton("Menu Del", callback_data="menu_del")],
        [InlineKeyboardButton("Menu Ban", callback_data="menu_ban")],
        [InlineKeyboardButton("Tutup", callback_data="close")],
    ]
    await message.reply_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))

@Bot.on_callback_query(filters.regex("menu_admin"))
async def menu_admin(client: Client, callback_query: CallbackQuery):
    admin_ids = await db.get_all_admins()
    if not admin_ids:
        admin_list = "<b><blockquote>❌ No admins found.</blockquote></b>"
    else:
        admin_list = "\n".join(f"<b><blockquote>ID: <code>{id}</code></blockquote></b>" for id in admin_ids)
    keyboard = [
        [InlineKeyboardButton("Tambah Admin", callback_data="tambah_admin")],
        [InlineKeyboardButton("Hapus Admin", callback_data="hapus_admin")],
        [InlineKeyboardButton("Kembali", callback_data="back_to_settings")],
    ]
    await callback_query.message.edit_text(f"<b>⚡ Current Admin List:</b>\n\n{admin_list}", reply_markup=InlineKeyboardMarkup(keyboard))
    await callback_query.answer()

@Bot.on_callback_query(filters.regex("menu_fsub"))
async def menu_fsub(client: Client, callback_query: CallbackQuery):
    fsub_ids = await db.get_all_fsub_ids()
    if not fsub_ids:
        fsub_list = "<b><blockquote>❌ No fsub ids found.</blockquote></b>"
    else:
        fsub_list = "\n".join(f"<b><blockquote>ID: <code>{id}</code></blockquote></b>" for id in fsub_ids)
    keyboard = [
        [InlineKeyboardButton("Tambah Fsub ID", callback_data="tambah_fsub_id")],
        [InlineKeyboardButton("Hapus Fsub ID", callback_data="hapus_fsub_id")],
        [InlineKeyboardButton("Kembali", callback_data="back_to_settings")],
    ]
    await callback_query.message.edit_text(f"<b>⚡ Current Fsub ID List:</b>\n\n{fsub_list}", reply_markup=InlineKeyboardMarkup(keyboard))
    await callback_query.answer()

@Bot.on_callback_query(filters.regex("menu_fsub_mode"))
async def menu_fsub_mode(client: Client, callback_query: CallbackQuery):
    fsub_mode = await db.get_fsub_mode()
    if fsub_mode:
        fsub_mode_status = "Aktif"
    else:
        fsub_mode_status = "Nonaktif"
    keyboard = [
        [InlineKeyboardButton(f"Ubah ke {'Nonaktif' if fsub_mode else 'Aktif'}", callback_data="ubah_fsub_mode")],
        [InlineKeyboardButton("Kembali", callback_data="back_to_settings")],
    ]
    await callback_query.message.edit_text(f"<b>⚡ Current Fsub Mode:</b> {fsub_mode_status}", reply_markup=InlineKeyboardMarkup(keyboard))
    await callback_query.answer()

@Bot.on_callback_query(filters.regex("menu_del"))
async def menu_del(client: Client, callback_query: CallbackQuery):
    del_time = await db.get_del_time()
    keyboard = [
        [InlineKeyboardButton("Ubah Waktu", callback_data="ubah_del_time")],
        [InlineKeyboardButton("Kembali", callback_data="back_to_settings")],
    ]
    await callback_query.message.edit_text(f"<b>⚡ Current Del Time:</b> {del_time} detik", reply_markup=InlineKeyboardMarkup(keyboard))
    await callback_query.answer()

@Bot.on_callback_query(filters.regex("menu_ban"))
async def menu_ban(client: Client, callback_query: CallbackQuery):
    ban_ids = await db.get_all_ban_ids()
    if not ban_ids:
        ban_list = "<b><blockquote>❌ No ban ids found.</blockquote></b>"
    else:
        ban_list = "\n".join(f"<b><blockquote>ID: <code>{id}</code></blockquote></b>" for id in ban_ids)
    keyboard = [
        [InlineKeyboardButton("Kembali", callback_data="back_to_settings")],
    ]
    await callback_query.message.edit_text(f"<b>⚡ Current Ban ID List:</b>\n\n{ban_list}", reply_markup=InlineKeyboardMarkup(keyboard))
    await callback_query.answer()
