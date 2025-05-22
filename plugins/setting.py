from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import db
from bot import Bot

@Bot.on_message(filters.command("settings"))
async def settings_command(client: Client, message: Message):
    keyboard = [
        [InlineKeyboardButton("Daftar Admin", callback_data="daftar_admin")],
        [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
        [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
        [InlineKeyboardButton("Tutup", callback_data="close")],
    ]
    msg = await message.reply_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))

@Bot.on_callback_query(filters.regex("daftar_admin"))
async def daftar_admin(client: Client, callback_query: CallbackQuery):
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

@Bot.on_callback_query(filters.regex("tambah_admin"))
async def tambah_admin(client: Client, callback_query: CallbackQuery):
    await callback_query.message.edit_text("Silakan masukkan ID admin baru:")
    await callback_query.answer()
    await client.listen(callback_query.from_user.id).then(
        lambda msg: tambah_admin_id(client, msg)
    )

async def tambah_admin_id(client: Client, message: Message):
    try:
        admin_id = int(message.text)
        await db.add_admin(admin_id)
        await message.reply_text("Admin baru berhasil ditambahkan!")
    except:
        await message.reply_text("Gagal menambahkan admin baru. Pastikan ID admin valid.")

@Bot.on_callback_query(filters.regex("hapus_admin"))
async def hapus_admin(client: Client, callback_query: CallbackQuery):
    admin_ids = await db.get_all_admins()
    if not admin_ids:
        await callback_query.message.edit_text("Tidak ada admin yang dapat dihapus.")
        await callback_query.answer()
    else:
        keyboard = []
        for admin_id in admin_ids:
            keyboard.append([InlineKeyboardButton(f"ID: {admin_id}", callback_data=f"hapus_admin_id_{admin_id}")])
        keyboard.append([InlineKeyboardButton("Kembali", callback_data="daftar_admin")])
        await callback_query.message.edit_text("Pilih admin yang ingin dihapus:", reply_markup=InlineKeyboardMarkup(keyboard))
        await callback_query.answer()

@Bot.on_callback_query(filters.regex("hapus_admin_id_(.*)"))
async def hapus_admin_id(client: Client, callback_query: CallbackQuery):
    admin_id = int(callback_query.data.split("_")[-1])
    await db.del_admin(admin_id)
    await callback_query.message.edit_text(f"Admin dengan ID {admin_id} berhasil dihapus.")
    await callback_query.answer()

@Bot.on_callback_query(filters.regex("back_to_settings"))
async def back_to_settings(client: Client, callback_query: CallbackQuery):
    keyboard = [
        [InlineKeyboardButton("Daftar Admin", callback_data="daftar_admin")],
        [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
        [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
        [InlineKeyboardButton("Tutup", callback_data="close")],
    ]
    await callback_query.message.edit_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))
    await callback_query.answer()
