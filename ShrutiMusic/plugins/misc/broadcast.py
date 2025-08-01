# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
#
# All rights reserved.
#
# This code is the intellectual property of Nand Yaduwanshi.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: badboy809075@gmail.com


import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

from ShrutiMusic import app
from ShrutiMusic.misc import SUDOERS
from ShrutiMusic.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from ShrutiMusic.utils.decorators.language import language
from ShrutiMusic.utils.formatters import alpha_to_int
from config import adminlist

# Add specific user IDs that can use the broadcast command
BROADCAST_ALLOWED_IDS = [6289700114, 7426116391]

IS_BROADCASTING = False


@app.on_message(filters.command(["broadcast", "reklam"]) & (filters.user(BROADCAST_ALLOWED_IDS) | SUDOERS))
@language
async def broadcast_message(client, message, _):
    global IS_BROADCASTING

    # Komut tetikleniyor mu kontrol için test mesajı
    await message.reply_text("Broadcast komutu çalıştı!")

    if IS_BROADCASTING:
        return await message.reply_text("Bir broadcast işlemi zaten devam ediyor, lütfen bekleyin.")

    if "-wfchat" in message.text or "-wfuser" in message.text:
        if not message.reply_to_message or not (message.reply_to_message.photo or message.reply_to_message.text):
            return await message.reply_text("Lütfen yayınlamak istediğiniz metin veya fotoğrafa yanıt verin.")

        if message.reply_to_message.photo:
            content_type = 'photo'
            file_id = message.reply_to_message.photo.file_id
        else:
            content_type = 'text'
            text_content = message.reply_to_message.text

        caption = message.reply_to_message.caption
        reply_markup = getattr(message.reply_to_message, 'reply_markup', None)

        IS_BROADCASTING = True
        await message.reply_text(_["broad_1"])

        if "-wfchat" in message.text:
            sent_chats = 0
            chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
            for chat_id in chats:
                try:
                    if content_type == 'photo':
                        await app.send_photo(chat_id=chat_id, photo=file_id, caption=caption, reply_markup=reply_markup)
                    else:
                        await app.send_message(chat_id=chat_id, text=text_content, reply_markup=reply_markup)
                    sent_chats += 1
                    await asyncio.sleep(0.2)
                except FloodWait as fw:
                    await asyncio.sleep(fw.x)
                except Exception as e:
                    # Hata varsa yazdırabiliriz, geliştirme için
                    print(f"Broadcast chat gönderim hatası: {e}")
                    continue
            await message.reply_text(f"Chatlere yayın tamamlandı! Toplam gönderilen: {sent_chats}.")

        if "-wfuser" in message.text:
            sent_users = 0
            users = [int(user["user_id"]) for user in await get_served_users()]
            for user_id in users:
                try:
                    if content_type == 'photo':
                        await app.send_photo(chat_id=user_id, photo=file_id, caption=caption, reply_markup=reply_markup)
                    else:
                        await app.send_message(chat_id=user_id, text=text_content, reply_markup=reply_markup)
                    sent_users += 1
                    await asyncio.sleep(0.2)
                except FloodWait as fw:
                    await asyncio.sleep(fw.x)
                except Exception as e:
                    print(f"Broadcast kullanıcı gönderim hatası: {e}")
                    continue
            await message.reply_text(f"Kullanıcılara yayın tamamlandı! Toplam gönderilen: {sent_users}.")

        IS_BROADCASTING = False
        return

    # Eğer yanıt yoksa mesajdan metin alma kısmı
    if message.reply_to_message:
        message_id = message.reply_to_message.id
        chat_id = message.chat.id
        reply_markup = getattr(message.reply_to_message, 'reply_markup', None)
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["broad_2"])
        query = message.text.split(None, 1)[1]
        for flag in ["-pin", "-nobot", "-pinloud", "-assistant", "-user"]:
            query = query.replace(flag, "")
        query = query.strip()
        if query == "":
            return await message.reply_text(_["broad_8"])

    IS_BROADCASTING = True
    await message.reply_text(_["broad_1"])

    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
        for chat_id in chats:
            try:
                if message.reply_to_message:
                    m = await app.copy_message(chat_id=chat_id, from_chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
                else:
                    m = await app.send_message(chat_id, text=query)

                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except:
                        pass
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except:
                        pass

                sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception as e:
                print(f"Broadcast gönderim hatası: {e}")
                continue
        try:
            await message.reply_text(_["broad_3"].format(sent, pin))
        except:
            pass

    if "-user" in message.text:
        susr = 0
        served_users = [int(user["user_id"]) for user in await get_served_users()]
        for user_id in served_users:
            try:
                if message.reply_to_message:
                    await app.copy_message(chat_id=user_id, from_chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
                else:
                    await app.send_message(user_id, text=query)
                susr += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception as e:
                print(f"Broadcast kullanıcı gönderim hatası: {e}")
                continue
        try:
            await message.reply_text(_["broad_4"].format(susr))
        except:
            pass

    if "-assistant" in message.text:
        aw = await message.reply_text(_["broad_5"])
        text = _["broad_6"]
        from ShrutiMusic.core.userbot import assistants

        for num in assistants:
            sent = 0
            client = await get_client(num)
            async for dialog in client.get_dialogs():
                try:
                    if message.reply_to_message:
                        await client.forward_messages(dialog.chat.id, chat_id, message_id)
                    else:
                        await client.send_message(dialog.chat.id, text=query)
                    sent += 1
                    await asyncio.sleep(3)
                except FloodWait as fw:
                    flood_time = int(fw.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
                except Exception as e:
                    print(f"Broadcast assistant gönderim hatası: {e}")
                    continue
            text += _["broad_7"].format(num, sent)
        try:
            await aw.edit_text(text)
        except:
            pass

    IS_BROADCASTING = False


async def auto_clean():
    while not await asyncio.sleep(10):
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    async for user in app.get_chat_members(
                        chat_id, filter=ChatMembersFilter.ADMINISTRATORS
                    ):
                        if user.privileges.can_manage_video_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except Exception as e:
            print(f"auto_clean hatası: {e}")
            continue


asyncio.create_task(auto_clean())
