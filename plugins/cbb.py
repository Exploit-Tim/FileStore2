# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
# All rights reserved.

from pyrogram import Client
from bot import Bot
from config import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import *

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "help":
        await query.message.edit_text(
            text=HELP_TXT.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                 InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
            ])
        )
    elif data == "about":
        await query.message.edit_text(
            text=ABOUT_TXT.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                 InlineKeyboardButton('ᴄʟᴏꜱᴇ', callback_data='close')]
            ])
        )
    elif data == "start":
        await query.message.edit_text(
            text=START_MSG.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help'),
                 InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data='about')]
            ])
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
    elif data == "daftar_admin":
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
        await query.message.edit_text(f"<b>⚡ Current Admin List:</b>\n\n{admin_list}", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "tambah_admin":
        await query.message.edit_text("Silakan masukkan ID admin baru:")
        response = await client.listen(query.from_user.id)
        try:
            admin_id = int(response.text)
            await db.add_admin(admin_id)
            await response.reply_text("Admin baru berhasil ditambahkan!")
            keyboard = [
                [InlineKeyboardButton("Daftar Admin", callback_data="daftar_admin")],
                [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
                [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
                [InlineKeyboardButton("Tutup", callback_data="close")],
            ]
            await response.reply_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            await response.reply_text("Gagal menambahkan admin baru. Pastikan ID admin valid.")
            keyboard = [
                [InlineKeyboardButton("Daftar Admin", callback_data="daftar_admin")],
                [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
                [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
                [InlineKeyboardButton("Tutup", callback_data="close")],
            ]
            await response.reply_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "hapus_admin":
        admin_ids = await db.get_all_admins()
        if not admin_ids:
            await query.message.edit_text("Tidak ada admin yang dapat dihapus.")
        else:
            keyboard = []
            for admin_id in admin_ids:
                keyboard.append([InlineKeyboardButton(f"ID: {admin_id}", callback_data=f"hapus_admin_id_{admin_id}")])
            keyboard.append([InlineKeyboardButton("Kembali", callback_data="daftar_admin")])
            await query.message.edit_text("Pilih admin yang ingin dihapus:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("hapus_admin_id_"):
        admin_id = int(data.split("_")[-1])
        await db.del_admin(admin_id)
        await query.message.edit_text(f"Admin dengan ID {admin_id} berhasil dihapus.")
        keyboard = [
            [InlineKeyboardButton("Daftar Admin", callback_data="daftar_admin")],
            [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
            [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
            [InlineKeyboardButton("Tutup", callback_data="close")],
        ]
        await query.message.reply_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "back_to_settings":
        keyboard = [
            [InlineKeyboardButton("Daftar Admin", callback_data="daftar_admin")],
            [InlineKeyboardButton("Daftar Fsub", callback_data="daftar_fsub")],
            [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
            [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
            [InlineKeyboardButton("Tutup", callback_data="close")],
        ]
        await query.message.edit_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))
   
    #=======#

    elif data == "daftar_fsub":
        channels = await db.show_channels()
        if not channels:
            channel_list = "<b><blockquote>❌ No channels found.</blockquote></b>"
        else:
            channel_list = "\n".join(f"<b><blockquote>ID: <code>{id}</code></blockquote></b>" for id in channels)
        keyboard = [
            [InlineKeyboardButton("Tambah Channel", callback_data="tambah_channel")],
            [InlineKeyboardButton("Hapus Channel", callback_data="hapus_channel")],
            [InlineKeyboardButton("Kembali", callback_data="back_to_settings")],
        ]
        await query.message.edit_text(f"<b>⚡ Current Channel List:</b>\n\n{channel_list}", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "tambah_channel":
        await query.message.edit_text("Silakan masukkan ID channel baru:")
        response = await client.listen(query.from_user.id)
        try:
            channel_id = int(response.text)
            await db.add_channel(channel_id)
            await response.reply_text("Channel baru berhasil ditambahkan!")
            keyboard = [
                [InlineKeyboardButton("Daftar Channel", callback_data="daftar_fsub")],
                [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
                [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
                [InlineKeyboardButton("Tutup", callback_data="close")],
            ]
            await response.reply_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            await response.reply_text("Gagal menambahkan channel baru. Pastikan ID channel valid.")
            keyboard = [
                [InlineKeyboardButton("Daftar Channel", callback_data="daftar_fsub")],
                [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
                [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
                [InlineKeyboardButton("Tutup", callback_data="close")],
            ]
            await response.reply_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "hapus_channel":
        channels = await db.show_channels()
        if not channels:
            await query.message.edit_text("Tidak ada channel yang dapat dihapus.")
        else:
            keyboard = []
            for channel_id in channels:
                keyboard.append([InlineKeyboardButton(f"ID: {channel_id}", callback_data=f"hapus_channel_id_{channel_id}")])
            keyboard.append([InlineKeyboardButton("Kembali", callback_data="daftar_fsub")])
            await query.message.edit_text("Pilih channel yang ingin dihapus:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("hapus_channel_id_"):
        channel_id = int(data.split("_")[-1])
        await db.rem_channel(channel_id)
        await query.message.edit_text(f"Channel dengan ID {channel_id} berhasil dihapus.")
        keyboard = [
            [InlineKeyboardButton("Daftar Channel", callback_data="daftar_fsub")],
            [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
            [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
            [InlineKeyboardButton("Tutup", callback_data="close")],
        ]
        await query.message.reply_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "back_to_settings":
        keyboard = [
            [InlineKeyboardButton("Daftar Admin", callback_data="daftar_admin")],
            [InlineKeyboardButton("Daftar Fsub", callback_data="daftar_fsub")],
            [InlineKeyboardButton("Set Welcome", callback_data="set_welcome")],
            [InlineKeyboardButton("Set Force Message", callback_data="set_force_msg")],
            [InlineKeyboardButton("Tutup", callback_data="close")],
        ]
        await query.message.edit_text("Menu Setting", reply_markup=InlineKeyboardMarkup(keyboard))

    #=======#
    
    elif data == "fsub_back":
        channels = await db.show_channels()
        buttons = []
        for cid in channels:
            try:
                chat = await client.get_chat(cid)
                mode = await db.get_channel_mode(cid)
                status = "🟢" if mode == "on" else "🔴"
                buttons.append([InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}")])
            except:
                continue
        await query.message.edit_text(
            "sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛs ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif data.startswith("rfs_ch_"):
        cid = int(data.split("_")[2])
        try:
            chat = await client.get_chat(cid)
            mode = await db.get_channel_mode(cid)
            status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏғғ"
            new_mode = "ᴏғғ" if mode == "on" else "on"
            buttons = [
                [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
            ]
            await query.message.edit_text(
                f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception:
            await query.answer("Failed to fetch channel info", show_alert=True)
    elif data.startswith("rfs_toggle_"):
        cid, action = data.split("_")[2:]
        cid = int(cid)
        mode = "on" if action == "on" else "off"
        await db.set_channel_mode(cid, mode)
        await query.answer(f"Force-Sub set to {'ON' if mode == 'on' else 'OFF'}")
        # Refresh the same channel's mode view
        chat = await client.get_chat(cid)
        status = "🟢 ON" if mode == "on" else "🔴 OFF"
        new_mode = "off" if mode == "on" else "on"
        buttons = [
            [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
        ]
        await query.message.edit_text(
            f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
