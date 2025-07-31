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
from pyrogram.enums import ChatMembersFilter, ParseMode
from pyrogram.errors import FloodWait
import random
import re

from ShrutiMusic import app

SPAM_CHATS = []
EMOJI = [
    "🦋🦋🦋🦋🦋",
    "🧚🌸🧋🍬🫖",
    "🥀🌷🌹🌺💐",
    "🌸🌿💮🌱🌵",
    "❤️💚💙💜🖤",
    "💓💕💞💗💖",
    "🌸💐🌺🌹🦋",
    "🍔🦪🍛🍲🥗",
    "🍎🍓🍒🍑🌶️",
    "🧋🥤🧋🥛🍷",
    "🍬🍭🧁🎂🍡",
    "🍨🧉🍺☕🍻",
    "🥪🥧🍦🍥🍚",
    "🫖☕🍹🍷🥛",
    "☕🧃🍩🍦🍙",
    "🍁🌾💮🍂🌿",
    "🌨️🌥️⛈️🌩️🌧️",
    "🌷🏵️🌸🌺💐",
    "💮🌼🌻🍀🍁",
    "🧟🦸🦹🧙👸",
    "🧅🍠🥕🌽🥦",
    "🐷🐹🐭🐨🐻‍❄️",
    "🦋🐇🐀🐈🐈‍⬛",
    "🌼🌳🌲🌴🌵",
    "🥩🍋🍐🍈🍇",
    "🍴🍽️🔪🍶🥃",
    "🕌🏰🏩⛩️🏩",
    "🎉🎊🎈🎂🎀",
    "🪴🌵🌴🌳🌲",
    "🎄🎋🎍🎑🎎",
    "🦅🦜🕊️🦤🦢",
    "🦤🦩🦚🦃🦆",
    "🐬🦭🦈🐋🐳",
    "🐔🐟🐠🐡🦐",
    "🦩🦀🦑🐙🦪",
    "🐦🦂🕷️🕸️🐚",
    "🥪🍰🥧🍨🍨",
    "🥬🍉🧁🧇🔮",
]

def clean_text(text):
    """Escape markdown special characters"""
    if not text:
        return ""
    return re.sub(r'([_*()~`>#+-=|{}.!])', r'\\1', text)

async def is_admin(chat_id, user_id):
    admin_ids = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    return user_id in admin_ids

async def process_members(chat_id, members, text=None, replied=None):
    tagged_members = 0
    usernum = 0
    usertxt = ""
    emoji_sequence = random.choice(EMOJI)
    emoji_index = 0
    
    for member in members:
        if chat_id not in SPAM_CHATS:
            break
        if member.user.is_deleted or member.user.is_bot:
            continue
            
        tagged_members += 1
        usernum += 1
        
        emoji = emoji_sequence[emoji_index % len(emoji_sequence)]
        usertxt += f"[{emoji}](tg://user?id={member.user.id}) "
        emoji_index += 1
        
        if usernum == 5:
            try:
                if replied:
                    await replied.reply_text(
                        usertxt,
                        disable_web_page_preview=True,
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    await app.send_message(
                        chat_id,
                        f"{text}\n{usertxt}",
                        disable_web_page_preview=True,
                        parse_mode=ParseMode.MARKDOWN
                    )
                await asyncio.sleep(2)  # Reduced sleep time to 2 seconds
                usernum = 0
                usertxt = ""
                emoji_sequence = random.choice(EMOJI)
                emoji_index = 0
            except FloodWait as e:
                await asyncio.sleep(e.value + 2)  # Extra buffer time
            except Exception as e:
                await app.send_message(chat_id, f"Error while tagging: {str(e)}")
                continue
    
    if usernum > 0 and chat_id in SPAM_CHATS:
        try:
            if replied:
                await replied.reply_text(
                    usertxt,
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await app.send_message(
                    chat_id,
                    f"{text}\n\n{usertxt}",
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.MARKDOWN
                )
        except Exception as e:
            await app.send_message(chat_id, f"Error sending final batch: {str(e)}")
    
    return tagged_members

@app.on_message(
    filters.command(["all", "allmention", "mentionall", "tagall"], prefixes=["/", "@"])
)
async def tag_all_users(_, message):
    admin = await is_admin(message.chat.id, message.from_user.id)
    if not admin:
        return await message.reply_text("Bu komutu yalnızca yöneticiler kullanabilir.")

    if message.chat.id in SPAM_CHATS:  
        return await message.reply_text(  
            "Etiketleme işlemi zaten çalışıyor. Durdurmak için /cancel komutunu kullan."  
        )  
    
    replied = message.reply_to_message  
    if len(message.command) < 2 and not replied:  
        return await message.reply_text(  
            "Herkesi etiketlemek için bir metin girin, örneğin: @all Merhaba arkadaşlar"  
        )  
    
    try:  
        # Get all members at once to avoid multiple iterations
        members = []
        async for m in app.get_chat_members(message.chat.id):
            members.append(m)
        
        total_members = len(members)
        SPAM_CHATS.append(message.chat.id)
        
        text = None
        if not replied:
            text = clean_text(message.text.split(None, 1)[1])
        
        tagged_members = await process_members(
            message.chat.id,
            members,
            text=text,
            replied=replied
        )
        
        summary_msg = f"""
Etiketleme tamamlandı ✅

Toplam üyeler: {total_members}
Etiketlenen üyeler: {tagged_members}
"""
        await app.send_message(message.chat.id, summary_msg)

    except FloodWait as e:  
        await asyncio.sleep(e.value)  
    except Exception as e:  
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")  
    finally:  
        try:  
            SPAM_CHATS.remove(message.chat.id)  
        except Exception:  
            pass

@app.on_message(
    filters.command(["admintag", "adminmention", "admins", "report"], prefixes=["/", "@"])
)
async def tag_all_admins(_, message):
    if not message.from_user:
        return

    admin = await is_admin(message.chat.id, message.from_user.id)  
    if not admin:  
        return await message.reply_text("Bu komutu yalnızca yöneticiler kullanabilir.")  

    if message.chat.id in SPAM_CHATS:  
        return await message.reply_text(  
            "Etiketleme işlemi zaten çalışıyor. Durdurmak için /cancel komutunu kullan."  
        )  
    
    replied = message.reply_to_message  
    if len(message.command) < 2 and not replied:  
        return await message.reply_text(  
            "Yöneticileri etiketlemek için bir metin girin, örneğin: @admins Merhaba Arkadaşlar"  
        )  
    
    try:  
        # Get all admins at once
        members = []
        async for m in app.get_chat_members(
            message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS  
        ):
            members.append(m)
        
        total_admins = len(members)
        SPAM_CHATS.append(message.chat.id)
        
        text = None
        if not replied:
            text = clean_text(message.text.split(None, 1)[1])
        
        tagged_admins = await process_members(
            message.chat.id,
            members,
            text=text,
            replied=replied
        )
        
        summary_msg = f"""
✅ Yönetici etiketleme işlemi başarıyla tamamlandı!

Toplam yöneticiler: {total_admins}
Etiketlenen yöneticiler: {tagged_admins}
"""
        await app.send_message(message.chat.id, summary_msg)

    except FloodWait as e:  
        await asyncio.sleep(e.value)  
    except Exception as e:  
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")  
    finally:  
        try:  
            SPAM_CHATS.remove(message.chat.id)  
        except Exception:  
            pass

@app.on_message(
    filters.command(
        [
            "stopmention",
            "cancel",
            "cancelmention",
            "offmention",
            "mentionoff",
            "cancelall",
        ],
        prefixes=["/", "@"],
    )
)
async def cancelcmd(_, message):
    chat_id = message.chat.id
    admin = await is_admin(chat_id, message.from_user.id)
    if not admin:
        return await message.reply_text("Only admins can use this command.")

    if chat_id in SPAM_CHATS:  
        try:  
            SPAM_CHATS.remove(chat_id)  
        except Exception:  
            pass  
        return await message.reply_text("Tagging process successfully stopped!")  
    else:  
        return await message.reply_text("No tagging process is currently running!")

MODULE = "Tᴀɢᴀʟʟ"
HELP = """
@all veya /all | /tagall veya @tagall | /mentionall veya @mentionall [metin] veya [herhangi bir mesaja yanıt]
- Grubunuzdaki tüm kullanıcıları rastgele emojilerle etiketler (her 5 kullanıcıda emoji değişir)

 /admintag veya @admintag | /adminmention veya @adminmention | /admins veya @admins [metin] veya [herhangi bir mesaja yanıt]
- Grubunuzdaki tüm yöneticileri rastgele emojilerle etiketler (her 5 kullanıcıda emoji değişir)

 /stopmention veya @stopmention | /cancel veya @cancel | /offmention veya @offmention | /mentionoff veya @mentionoff | /cancelall veya @cancelall
- Çalışan herhangi bir etiketleme işlemini durdurur

Notlar:
1. Bu komutları sadece yöneticiler kullanabilir
2. Bot ve yardımcı botunuz grubunuzda yönetici olmalıdır
3. Kullanıcılar profillerine bağlantılı rastgele emojilerle etiketlenecektir
4. İşlem tamamlandığında, size özet ve sayılar gösterilecektir
5. Her seferde 5 kullanıcı etiketlenir ve her grup için benzersiz emoji dizisi kullanılır
