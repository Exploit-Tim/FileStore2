# RT# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
# All rights reserved.

from pyrogram import Client
from bot import Bot
from config import *
from pyrogram.types import Message, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import *
from pyrogram.enums import ParseMode, ChatAction, ChatMemberStatus, ChatType
import speedtest
import time

start_time = time.time()

def format_uptime(uptime):
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

async def get_server_info():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        st.download()
        st.upload()
        result = st.results.dict()

        uptime = timedelta(seconds=time.time() - start_time)
        uptime_str = format_uptime(uptime)

        info = f"""
<b>📊 Server Info</b>
<blockquote>⏰ Uptime: {uptime_str}</blockquote>
<b>📈 Speedtest Results</b>
<blockquote>👥 <b>Client :</b>
⟡ ISP: {result['client']['isp']}
⟡ Country: {result['client']['country']}
🏢 <b>Server :</b>
⟡ Name: {result['server']['name']}
⟡ Country: {result['server']['country']}, {result['server']['cc']}
⟡ Sponsor: {result['server']['sponsor']}
⟡ Ping: {result['ping']}
⟡ Download: {round(result['download'] / 1024 / 1024, 2)} Mbps
⟡ Upload: {round(result['upload'] / 1024 / 1024, 2)} Mbps</blockquote>
"""
        return info
    except Exception as e:
        return f"<b>❌ Error:</b> <code>{e}</code>"


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
        except:
            await response.reply_text("Gagal menambahkan admin baru. Pastikan ID admin valid.")

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
        await query.message.edit_text("<b>𝗠𝗲𝗻𝘂 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀</b>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "hapus_admin":
        admin_ids = await db.get_all_admins()
        if not admin_ids:
            await query.message.edit_text("Tidak ada admin yang dapat dihapus.")
        else:
            keyboard = [[InlineKeyboardButton(f"ID: {admin_id}", callback_data=f"hapus_admin_id_{admin_id}")] for admin_id in admin_ids]
            keyboard.append([InlineKeyboardButton("Kembali", callback_data="daftar_admin")])
            await query.message.edit_text("Pilih admin yang ingin dihapus:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("hapus_admin_id_"):
        admin_id = int(data.split("_")[-1])
        await db.del_admin(admin_id)
        await query.message.edit_text(f"Admin dengan ID {admin_id} berhasil dihapus.")
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
        await query.message.edit_text("<b>𝗠𝗲𝗻𝘂 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀</b>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif data == "daftar_fsub":
         channels = await db.show_channels()
         if not channels:
             channel_list = "❌ <b>Tidak ada channel yang ditambahkan.</b>"
         else:
             channel_list = ""
         for ch_id in channels:
            try:
                chat = await client.get_chat(ch_id)
                channel_list += f"🔹 <b>{chat.title}</b>\n<code>{ch_id}</code>\n\n"
            except:
                channel_list += f"⚠️ <b>Unknown Channel</b>\n<code>{ch_id}</code>\n\n"

         keyboard = [
             [InlineKeyboardButton("Tambah Channel", callback_data="tambah_channel")],
             [InlineKeyboardButton("Hapus Channel", callback_data="hapus_channel")],
             [InlineKeyboardButton("Kembali", callback_data="back_to_settings")],
         ]

         await query.message.edit_text(
              f"<b>⚡ Daftar Channel Saat Ini:</b>\n\n{channel_list}",
               reply_markup=InlineKeyboardMarkup(keyboard)
               )

    elif data == "tambah_channel":
        await query.message.edit_text(
            "Silakan masukkan ID channel baru (gunakan tanda minus, misal: <code>-1001234567890</code>):"
        )
        response = await client.listen(query.from_user.id)

        temp = await response.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)

        try:
            channel_id = int(response.text)
        except ValueError:
            return await temp.edit("<b>❌ Invalid Channel ID!</b>")

        # Cek apakah channel sudah ada
        all_channels = await db.show_channels()
        channel_ids_only = [cid if isinstance(cid, int) else cid[0] for cid in all_channels]
        if channel_id in channel_ids_only:
            return await temp.edit(f"<b>Channel already exists:</b> <code>{channel_id}</code>")

        try:
            chat = await client.get_chat(channel_id)

            if chat.type != ChatType.CHANNEL:
                return await temp.edit("<b>❌ Only public or private channels are allowed.</b>")

            member = await client.get_chat_member(chat.id, "me")

            if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await temp.edit("<b>❌ Bot must be an admin in that channel.</b>")

            # Ambil link undangan channel
            try:
                link = await client.export_chat_invite_link(chat.id)
            except Exception:
                link = f"https://t.me/{chat.username}" if chat.username else f"https://t.me/c/{str(chat.id)[4:]}"

            await db.add_channel(channel_id)

            await temp.edit(
                f"<b>✅ Force-sub channel added successfully!</b>\n\n"
                f"<b>Name:</b> <a href='{link}'>{chat.title}</a>\n"
                f"<b>ID:</b> <code>{channel_id}</code>",
                disable_web_page_preview=True
            )

        except Exception as e:
            await temp.edit(
                f"<b>❌ Failed to add channel:</b>\n<code>{channel_id}</code>\n\n<i>{e}</i>"
            )

        # Tampilkan kembali menu pengaturan
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
        await query.message.edit_text("<b>𝗠𝗲𝗻𝘂 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀</b>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "hapus_channel":
        channels = await db.show_channels()
        if not channels:
            await query.message.edit_text("Tidak ada channel yang dapat dihapus.")
        else:
            keyboard = [[InlineKeyboardButton(f"ID: {channel_id}", callback_data=f"hapus_channel_id_{channel_id}")] for channel_id in channels]
            keyboard.append([InlineKeyboardButton("Kembali", callback_data="daftar_fsub")])
            await query.message.edit_text("Pilih channel yang ingin dihapus:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("hapus_channel_id_"):
        channel_id = int(data.split("_")[-1])
        await db.rem_channel(channel_id)
        await query.message.edit_text(f"Channel dengan ID {channel_id} berhasil dihapus.")
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
        await query.message.edit_text("<b>𝗠𝗲𝗻𝘂 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀</b>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    
    elif data == "Mode_fsub":
        channels = await db.show_channels()
        if not channels:
            return await query.message.edit_text(
                "<b>❌ Tidak ada channel yang ditambahkan.</b>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Kembali", callback_data="back_to_settings")]
                ])
            )
        buttons = []
        for ch_id in channels:
            try:
                chat = await client.get_chat(ch_id)
                mode = await db.get_channel_mode(ch_id)
                status = "🟢 ON" if mode == "on" else "🔴 OFF"
                title = f"{chat.title} [{status}]"
                buttons.append([InlineKeyboardButton(title, callback_data=f"toggle_mode_{ch_id}")])
            except:
                buttons.append([InlineKeyboardButton(f"⚠️ {ch_id} (Error)", callback_data=f"toggle_mode_{ch_id}")])

        buttons.append([InlineKeyboardButton("Kembali", callback_data="back_to_settings")])

        await query.message.edit_text(
            "<b>⚙️ Mode Fsub per Channel</b>\n"
            "<i>Klik nama channel untuk mengaktifkan/nonaktifkan mode Fsub:</i>\n\n"
            "🟢 = Aktif\n🔴 = Tidak aktif",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data.startswith("toggle_mode_"):
        ch_id = int(data.split("_")[-1])
        current_mode = await db.get_channel_mode(ch_id)
        new_mode = "off" if current_mode == "on" else "on"
        await db.set_channel_mode(ch_id, new_mode)

        # Refresh tampilan Mode_fsub
        channels = await db.show_channels()
        buttons = []
        for channel_id in channels:
            try:
                chat = await client.get_chat(channel_id)
                mode = await db.get_channel_mode(channel_id)
                status = "🟢 ON" if mode == "on" else "🔴 OFF"
                title = f"{chat.title} [{status}]"
                buttons.append([InlineKeyboardButton(title, callback_data=f"toggle_mode_{channel_id}")])
            except:
                buttons.append([InlineKeyboardButton(f"⚠️ {channel_id} (Error)", callback_data=f"toggle_mode_{channel_id}")])

        buttons.append([InlineKeyboardButton("Kembali", callback_data="back_to_settings")])

        await query.message.edit_text(
            "<b>⚙️ Mode Fsub per Channel</b>\n"
            "<i>Klik nama channel untuk mengaktifkan/nonaktifkan mode Fsub:</i>\n\n"
            "🟢 = Aktif\n🔴 = Tidak aktif",
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

    elif data in ["back_to_settings", "fsub_back"]:
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
        await query.message.edit_text("<b>𝗠𝗲𝗻𝘂 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀</b>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    
    elif data == "time_delete":
        current_time = await db.get_del_timer()
        await query.message.edit_text(
            f"<b>⏱ Current Delete Timer:</b> <code>{current_time}</code> seconds\n\n"
            "To change it, send the number of seconds as a reply to this message.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("‹ Back", callback_data="back_to_settings")]
            ])
        )

        # Tunggu input pengguna
        response = await client.listen(query.from_user.id)

        try:
            duration = int(response.text)
            await db.set_del_timer(duration)
            await response.reply(f"<b>✅ Delete timer updated to {duration} seconds.</b>")
        except ValueError:
            await response.reply("<b>❌ Invalid number. Please send a valid duration in seconds.</b>")

        # Tampilkan ulang menu
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
        await query.message.edit_text("<b>𝗠𝗲𝗻𝘂 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀</b>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    
    elif data == "server_info":
        await query.message.edit_text(
            "<b>🔄 Mengambil informasi server...</b>"
        )
        result = await get_server_info()
        await query.message.edit_text(
            result,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_info")],
                [InlineKeyboardButton("‹ Kembali", callback_data="back_to_settings")]
            ])
        )

    elif data == "refresh_info":
        await query.answer("Memuat ulang...")
        result = await get_server_info()

        await query.message.edit_text(
            result,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_info")],
                [InlineKeyboardButton("‹ Kembali", callback_data="back_to_settings")]
            ])
        )

    elif data == "konten":
        channels = await db.show_channels()
        keyboard = []
    
        if not channels:
            text = "<b>📢 Channel konten belum ada.</b>\n\nSilakan tambahkan channel konten terlebih dahulu."
            keyboard.append([InlineKeyboardButton("➕ Tambah Konten", callback_data="konten_add")])
        else:
            text = "<b>📢 Daftar Channel Konten:</b>\nKlik ID channel untuk melihat detail atau mengganti."
    
            for ch_id in channels:
                try:
                    chat = await client.get_chat(ch_id)
                    btn_text = f"{chat.title} ({ch_id})"
                except Exception:
                    btn_text = f"⚠️ Channel Tidak Terdeteksi ({ch_id})"
    
                keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"konten_info:{ch_id}")])
    
            keyboard.append([InlineKeyboardButton("➕ Tambah Konten", callback_data="konten_add")])
    
        keyboard.append([InlineKeyboardButton("‹ Kembali", callback_data="back_to_settings")])
        await query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("konten_info:"):
        ch_id = int(data.split(":")[1])
        try:
            chat = await client.get_chat(ch_id)
            text = (
                f"<b>📢 Info Channel:</b>\n"
                f"• Nama: <b>{chat.title}</b>\n"
                f"• ID: <code>{ch_id}</code>\n\n"
                f"Ingin mengganti channel ini?"
            )
        except Exception:
            text = f"⚠️ Channel tidak ditemukan untuk ID <code>{ch_id}</code>\nIngin mengganti dengan channel lain?"
    
        keyboard = [
            [InlineKeyboardButton("🔁 Ganti", callback_data="konten_add")],
            [InlineKeyboardButton("‹ Kembali", callback_data="konten")],
        ]
        await query.message.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "konten_add":
        await query.message.edit_text(
            "Masukkan ID channel konten (format seperti <code>-1001234567890</code>):",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("‹ Batal", callback_data="konten")]
            ])
        )
    
        response = await client.listen(query.from_user.id)  # tanpa timeout
    
        if response.text == "/cancel" or response.text.lower() in ["batal", "kembali"]:
            await query.message.reply_text("❌ Dibatalkan.", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("‹ Kembali", callback_data="konten")]
            ]))
            return
    
        try:
            new_konten_id = int(response.text)
            chat = await client.get_chat(new_konten_id)
    
            if chat.type != ChatType.CHANNEL:
                raise ValueError("Bukan channel.")
    
            member = await client.get_chat_member(chat.id, "me")
            if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                raise ValueError("Bot bukan admin.")
    
            await db.add_konten_channel_id(new_konten_id)
            await response.reply_text(
                f"✅ Channel berhasil ditambahkan: <b>{chat.title}</b>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("‹ Kembali", callback_data="konten")]
                ])
            )
    
        except Exception as e:
            await response.reply_text(
                f"❌ Gagal menambahkan channel: {e}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("‹ Kembali", callback_data="konten")]
                ])
            )

#MENU PICT

    # Menu utama untuk Pict
    if data == "menu_pict":
        keyboard = [
            [InlineKeyboardButton("📸 Pict Welcome", callback_data="show_welcome_pict")],
            [InlineKeyboardButton("🔐 Pict Force", callback_data="show_force_pict")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="back_to_settings")]
        ]
        await query.message.edit_text(
            "<b>🖼 Pilih jenis gambar untuk ditampilkan atau diganti link-nya.</b>",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # Menampilkan Welcome Pict
    elif data == "show_welcome_pict":
        links = await db.get_pict_links()
        keyboard = [
            [InlineKeyboardButton("🔁 Ganti Link", callback_data="change_welcome_link")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="menu_pict")]
        ]
        await query.message.edit_media(
            media=InputMediaPhoto(
                media=links["welcome"],
                caption=f"<b>🌄 Link Aktif:</b>\n{links['welcome']}"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # Menampilkan Force Pict
    elif data == "show_force_pict":
        links = await db.get_pict_links()
        keyboard = [
            [InlineKeyboardButton("🔁 Ganti Link", callback_data="change_force_link")],
            [InlineKeyboardButton("🔙 Kembali", callback_data="menu_pict")]
        ]
        await query.message.edit_media(
            media=InputMediaPhoto(
                media=links["force"],
                caption=f"<b>🔒 Link Aktif:</b>\n{links['force']}"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # Ganti link Welcome Pict
    elif data == "change_welcome_link":
        await query.message.edit_text("📝 Kirim link baru untuk <b>Pict Welcome</b>:")
        response = await client.listen(query.from_user.id)
        await db.set_pict_link("welcome", response.text)
        await response.reply_text(
            "✅ Link Pict Welcome berhasil diubah!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data="menu_pict")]])
        )

    # Ganti link Force Pict
    elif data == "change_force_link":
        await query.message.edit_text("📝 Kirim link baru untuk <b>Pict Force</b>:")
        response = await client.listen(query.from_user.id)
        await db.set_pict_link("force", response.text)
        await response.reply_text(
            "✅ Link Pict Force berhasil diubah!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Kembali", callback_data="menu_pict")]])
        )
            
    elif data == "back_to_settings":
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
        await query.message.edit_text("<b>𝗠𝗲𝗻𝘂 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀</b>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))


    elif data == "db_id":
        await query.message.edit_text("Belum tersedia.")

    elif data == "db_url":
        await query.message.edit_text("Belum tersedia.")

    elif data == "protect":
        await query.message.edit_text("Belum tersedia.")

    elif data == "custom_caption":
        await query.message.edit_text("Belum tersedia.")

    elif data == "konen":
        await query.message.edit_text("Belum tersedia.")
