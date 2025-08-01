import asyncio
import random
from pyrogram import filters
from pyrogram.types import Message
from ShrutiMusic import app  # Senin pyrogram Client nesnen

# Aktif etiketleme takibi (chat_id: True)
active_chats = {}

# Mesaj listeleri (her biri 20 mesaj içeriyor, önceki mesajda hazırlandı)
GM_MESSAGES = [
    "🌞 Gᴜ̈ɴᴀʏᴅıɴ {mention} ☀️", "🌤️ Hᴀᴅɪ ᴜʏᴀɴ {mention}", "🌸 Gᴜ̈ɴᴇ ʙɪʀɪɴᴄɪ ᴀᴅıᴍ: {mention}",
    "⏰ Uʏᴀɴᴍᴀ ᴢᴀᴍᴀɴı {mention}", "☕ Kᴀʜᴠᴇᴍ Hᴀᴢıʀ {mention}!", "🌅 Yᴇɴɪ ɢᴜ̈ɴ Yᴇɴɪ ᴜᴍᴜᴛʟᴀʀ",
    "🌈 Gᴜ̈ɴᴇşʟɪ ʙɪʀ ɢᴜ̈ɴ {mention}!", "🐓 Hᴏʀᴏᴢʟᴀʀ Öᴛᴛᴜ {mention}!", "📣 Sᴇɴsɪᴢ ᴏʟᴍᴀᴢ {mention}!",
    "🕊️ Hᴜᴢᴜʀʟᴜ sᴀʙᴀʜʟᴀʀ", "📆 Yᴇɴɪ ɢᴜ̈ɴᴇ ʜᴀᴢıʀ ᴍıʏıᴢ {mention}?", "🎉 Eʀᴋᴇɴ ᴋᴀʟᴋᴀɴ ʏᴏʟ ᴀʟıʀ",
    "🌇 Gᴜ̈ɴᴇ ᴍᴇʀʜᴀʙᴀ ᴅᴇ!", "🌟 Uʏᴀɴᴀʟıᴍ ᴅᴏsᴛʟᴀʀ!", "🚿 Dɪşʟᴇʀɪɴɪ ғıʀçᴀʟᴀ {mention} 😁",
    "🎶 Mᴜ̈ᴢɪᴋ Aᴄ̧ ᴏʏᴀɴ {mention}", "☀️ Gᴜ̈ɴᴇɴɪɴ ɢᴜ̈ᴢᴇʟ ʙᴀşʟᴀsıɴ!", "📢 Aʏʟᴀɴᴅɪɴɪᴢ ᴍı?",
    "💼 İşᴇ ɢɪᴅᴇɴʟᴇʀ ᴜʏᴀɴɪɴ", "👀 {mention} Kᴀʟᴋ ʙᴀᴋᴀʟɪᴍ!"
]

GN_MESSAGES = [
    "🌙 İʏɪ Gᴇᴄᴇʟᴇʀ {mention}", "💤 Tᴀᴛʟı ʀᴜʏᴀʟᴀʀ {mention}", "🌌 Gᴇᴄᴇɴɪɴ sᴀᴋɪɴʟɪɢ̆ɪ ᴛᴀʀᴀғıɴᴅᴀ",
    "🛏️ Uʏᴋᴜ Zᴀᴍᴀɴı {mention}", "🧸 Sᴀɴᴀ ʙɪʀ ᴍᴀsᴀʟ", "🌠 Hᴀʏᴀʟʟᴀʀıɴ ɢᴜ̈ᴢᴇʟ ᴏʟsᴜɴ",
    "🎧 Hᴀfɪғ ᴍᴜ̈ᴢɪᴋ ᴀç ᴜʏᴋᴜʏᴀ ᴅᴀʟ", "📚 Kɪᴛᴀᴘʟᴀʀɪɴı Kᴀᴘᴀᴛ {mention}",
    "💤 Zᴢᴢ... Gᴇᴄᴇʏɪ ᴘᴀʀʟᴀᴛᴀɴ ᴋᴀɴᴀᴛʟᴀʀ", "🐑 Bɪʀ, ɪᴋɪ, ᴜ̈ç... Uʏᴋᴜɴ ɢᴇʟᴅɪ ᴍɪ?",
    "🕯️ Lᴀᴍʙᴀʏı sᴏ̈ɴᴅᴜ̈ʀ {mention}", "🌜 Mᴇʜᴛᴀᴘ ᴀʟᴛɪɴᴅᴀ ʜᴜᴢᴜʀ", "😴 Kᴀғᴀɴı ʏᴀsʟᴀ ʀᴀʜᴀᴛʟᴀ",
    "⏳ Yᴀʀıɴᴀ ᴋᴀᴅᴀʀ ᴠᴇᴅᴀ", "🖤 Gᴇᴄᴇʟᴇʀɪɴ ᴛᴇɴʜᴀ ʜᴜᴢᴜʀᴜ", "🪶 Uʏᴋᴜ ᴘᴇʀɪʟᴇʀɪ sᴇɴɪɴʟᴇ",
    "👁️‍🗨️ Kᴀᴘᴀɴɪ ɢᴏ̈ᴢʟᴇʀɪɴɪɴ ᴅᴇʀɪɴʟɪɢ̆ɪɴᴇ", "💤 İʏɪ ᴅɪɴʟᴇɴᴍᴇʟᴇʀ", "🐱 Kᴇᴅɪ sᴇɴɪɴʟᴇ ᴜʏᴜʏᴏʀ",
    "🎈 Rᴜʏᴀʟᴀʀ ᴀʟᴇᴍɪɴᴇ ʏᴏʟᴄᴜʟᴜᴋ"
]

ST_MESSAGES = [
    "💬 Sᴏʜʙᴇᴛ ᴠᴀʀ! {mention}", "📢 Sᴇɴsɪᴢ ᴏʟᴍᴀᴢ {mention}", "🔥 Kᴏɴᴜ Aᴄ̧ıʟᴅı, Gᴇʟ!",
    "💭 ʙɪʀ ғɪᴋɪʀɪɴ ᴠᴀʀ mı?", "🗣️ Sᴏ̈ᴢ sɪʀᴀsı sᴇɴᴅᴇ!", "🎤 Mɪᴋʀᴏғᴏɴ sᴇɴᴅᴇ",
    "👀 Hᴇʀᴋᴇs sᴇɴɪ ʙᴇᴋʟɪʏᴏʀ", "📱 Tᴇʟᴇғᴏɴᴜ ᴇʟɪɴᴇ ᴀʟ", "🫣 Sᴀᴋʟᴀɴᴍᴀ, Gᴇʟ",
    "🍿 Mᴇʀᴀᴋ ᴇᴛᴛɪᴋ ʏᴀ, Gᴇʟ ᴀɴʟᴀᴛ", "📲 ᴀᴋᴛɪғ ᴏʟ", "🎯 Kᴏɴᴜʏᴀ ᴅᴀʜɪʟ ᴏʟ",
    "⚡ Gᴇʟɪɴʟᴇʀ Gᴇʟɪɴʟᴇʀ", "🥳 Sᴏʜʙᴇᴛᴇ Nᴇşe Kᴀᴛ", "🎮 Gᴇʟ ʙɪʀ ᴏʏᴜɴ ᴏʏɴᴀʏᴀʟıᴍ",
    "🧠 Zᴇᴋᴀ Sᴀᴠᴀşɪ ʙᴀşʟɪʏᴏʀ", "📷 Sᴏʜʙᴇᴛᴇ ғᴏᴛᴏ ᴀᴛ", "🎵 Mᴜ̈ᴢɪᴋᴛᴇɴ sᴏ̈ᴢ ᴀᴄ̧",
    "🔔 Hᴀᴅɪ Kᴀᴛıʟ", "🧩 Sᴏʀᴜ Cᴇᴠᴀᴘ ʙᴀşʟᴀᴅı!"
]

KT_MESSAGES = [
    "🐺 Kᴜʀᴛʟᴀʀ ᴀʀᴀsıɴᴅᴀsıɴ {mention}", "🌕 Aʏ ʏᴜ̈ᴋsᴇʟɪʏᴏʀ", "💀 Kɪᴍ Kɪᴍɪ ʏɪʏᴇᴄᴇᴋ?",
    "🔪 Rᴏʟʟᴇʀ ᴅᴀɢ̆ıᴛıʟᴅı", "🧛 Vᴀᴍᴘɪʀʟᴇʀ ʜᴀʀᴇᴋᴇᴛᴇ ɢᴇçᴛɪ", "🔍 Dᴇᴛᴇᴋᴛɪғ ɪş ʙᴀşɪɴᴅᴀ",
    "🎭 Hᴇʀ ᴋᴇş ʙɪʀ ʀᴏʟᴅᴇ", "⏳ Gᴇᴄᴇ ᴏʟᴅᴜ, Sᴜsᴜɴ!", "☀️ Gᴜ̈ɴᴅᴜᴢ Gᴇʟᴅɪ, Oʏʟᴀᴍᴀ Bᴀşʟᴀᴅı",
    "👁️ Sᴇɴɪɴ Rᴏʟᴜ̈ɴɴᴇ Nᴇ?", "🔥 Aᴛᴇş ʏᴀɴᴅı, Kɪᴍ Yᴀɴᴀᴄᴀᴋ?"
]

# Kullanıcıları teker teker etiketleme fonksiyonu
async def tag_users_individual(chat_id, messages, tag_type):
    users = []
    async for member in app.get_chat_members(chat_id):
        if member.user.is_bot or member.user.is_deleted:
            continue
        users.append(member.user)
    total = len(users)
    tagged_count = 0

    for user in users:
        if chat_id not in active_chats:
            # Durdurma isteği var, çık
            break
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        msg = random.choice(messages).format(mention=mention)
        await app.send_message(chat_id, msg, disable_web_page_preview=True, parse_mode="markdown")
        tagged_count += 1
        await asyncio.sleep(2)  # spam engelleme için bekle

    # Etiketleme tamamlandı mesajı
    if chat_id in active_chats:
        del active_chats[chat_id]
        await app.send_message(
            chat_id,
            f"✅ **{tag_type} etiketleme tamamlandı!**\n\n"
            f"Toplam kullanıcı: {total}\n"
            f"Etiketlenen kullanıcı: {tagged_count}"
        )

# Komutlar

@app.on_message(filters.command("gtag") & filters.group)
async def gtag_start(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        await message.reply("⚠️ Günaydın etiketleme zaten devam ediyor.")
        return
    active_chats[chat_id] = True
    await message.reply("☀️ Günaydın etiketleme başlatıldı...")
    await tag_users_individual(chat_id, GM_MESSAGES, "Günaydın")

@app.on_message(filters.command("itag") & filters.group)
async def itag_start(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        await message.reply("⚠️ İyi geceler etiketleme zaten devam ediyor.")
        return
    active_chats[chat_id] = True
    await message.reply("🌙 İyi geceler etiketleme başlatıldı...")
    await tag_users_individual(chat_id, GN_MESSAGES, "İyi Geceler")

@app.on_message(filters.command("stag") & filters.group)
async def stag_start(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        await message.reply("⚠️ Sohbete çağırma etiketleme zaten devam ediyor.")
        return
    active_chats[chat_id] = True
    await message.reply("💬 Sohbete çağırma etiketleme başlatıldı...")
    await tag_users_individual(chat_id, ST_MESSAGES, "Sohbete Çağırma")

@app.on_message(filters.command("ktag") & filters.group)
async def ktag_start(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        await message.reply("⚠️ Kurt oyunu etiketleme zaten devam ediyor.")
        return
    active_chats[chat_id] = True
    await message.reply("🐺 Kurt oyunu etiketleme başlatıldı...")
    await tag_users_individual(chat_id, KT_MESSAGES, "Kurt Oyunu")

# Durdurma komutları (birden fazla isimle)

STOP_COMMANDS = ["stopall", "gmstop", "istop", "ststop", "kstop", "iptal", "cancel", "durdur"]

@app.on_message(filters.command(STOP_COMMANDS) & filters.group)
async def stop_tagging(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 Etiketleme durduruldu.")
    else:
        await message.reply("❌ Aktif bir etiketleme bulunamadı.")

# Yardım komutu

@app.on_message(filters.command("taghelp") & filters.group)
async def taghelp(_, message: Message):
    help_text = """
🏷️ **Etiketleme Komutları Yardımı**

**🌞 Günaydın:**
• `/gtag` - Günaydın mesajlarıyla etiketleme başlatır  
• `/gmstop` - Günaydın etiketlemeyi durdurur

**🌙 İyi Geceler:**
• `/itag` - İyi geceler mesajlarıyla etiketleme başlatır  
• `/istop` - İyi geceler etiketlemeyi durdurur

**💬 Sohbete Çağırma:**
• `/stag` - Sohbete çağırma başlatır  
• `/ststop` - Sohbete çağırmayı durdurur

**🐺 Kurt Oyunu:**
• `/ktag` - Kurt oyununa özel etiketleme başlatır  
• `/kstop` - Kurt etiketlemeyi durdurur

**🛑 Genel:**
• `/stopall`, `/iptal`, `/cancel`, `/durdur` - Tüm etiketlemeleri durdurur  
• `/taghelp` - Bu yardım mesajını gösterir

📌 *Not:* Her sohbette aynı anda yalnızca bir etiketleme aktif olabilir.
"""
    await message.reply(help_text)
