import asyncio
import random
from pyrogram import filters
from pyrogram.types import Message
from pyrogram import enums
from ShrutiMusic import app

active_chats = {}

# Günaydın Mesajları
GTAG_MESSAGES = [
    "🌞 Günaydın! ☀️\n\n{mention} Haydi yeni güne enerjik başlayalım!",
    "☀️ Gün ışığına merhaba! {mention} Güzel bir gün olsun!",
    "🌻 Günaydın {mention}, yeni umutlarla dolu olsun bugün!",
    "💫 Mutlu sabahlar {mention}! Harika bir gün dilerim.",
    "🌅 Güne güzel başlayalım {mention}, başarılar!",
    "🌸 Sabahın tazeliği gibi güzel olsun günün {mention}!",
    "🎵 Güne güzel melodilerle başla {mention}!",
    "🌟 Yeni bir gün, yeni fırsatlar {mention}!",
    "🌈 Günaydın {mention}, yüzün hep gülsün!",
    "🍃 Taze başlangıçlara hazır mısın {mention}?"
]

# İyi Geceler Mesajları (itag komutunda kullanılacak)
ITAG_MESSAGES = [
    "🌙 İyi geceler {mention}, tatlı rüyalar!",
    "✨ Huzurlu ve güzel bir uyku seni bekliyor {mention}.",
    "💤 Günün yorgunluğunu bırak ve rahatla {mention}.",
    "🌌 Yıldızlar kadar parlak rüyalar {mention}!",
    "🌟 İyi geceler {mention}, yarın yeni umutlarla dolu olsun!",
    "🛌 Tatlı düşler, iyi geceler {mention}!",
    "🌠 Gecenin sessizliği sana huzur getirsin {mention}.",
    "🕯️ Dinlen, yenilen ve güzel uyan {mention}.",
    "🌺 Geceyi sevgiyle kucakla {mention}, iyi geceler!",
    "🌛 Rüyaların gerçek olsun {mention}!"
]

# Sohbete Çağırma Mesajları (stag komutunda kullanılacak)
STAG_MESSAGES = [
    "🎉 Hey {mention}, sohbet başlasın!",
    "🔥 {mention}, hadi grupta hareketlenme zamanı!",
    "💬 Sohbet ateşini yakalım {mention}!",
    "🚀 Enerjini göster {mention}, muhabbet başlasın!",
    "🌟 Arkadaşlar, {mention} geldi, sohbet kaldığı yerden devam!",
    "🎊 Grupta eğlence başlasın, {mention} sizlerle!",
    "💥 Hey {mention}, ses ver hadi!",
    "👋 Selam {mention}, sohbet zamanı!",
    "🎈 Muhtemelen sen de can sıkıntısını yendin {mention}!",
    "🌈 Haydi herkes hazır olsun, {mention} sesleniyor!"
]

# Kurt Oyununa Çağırma Mesajları
KTAG_MESSAGES = [
    "🐺 Hey {mention}, kurt oyununa katılmaya ne dersin?",
    "🌕 Gecenin sessizliğinde kurtlar uluyor! {mention} seni bekliyor.",
    "🎲 Kurt oyun zamanı! {mention} hadi grupta buluşalım.",
    "🔥 Stratejini göster {mention}, kurt oyununa davetlisin!",
    "⚔️ Takım kur, plan yap ve kazan {mention}!",
    "🏹 Hadi, cesur kurtlar aramıza katılsın! {mention}",
    "🎉 Heyecan dolu kurt oyunu başladı, {mention} sen de katıl!",
    "🕹️ Oyun zamanı {mention}, yerini al!",
    "🌲 Ormanın kurdu sensin {mention}, göster kendini!",
    "⚡ Kurt oyununda seninle güçlenelim {mention}!"
]

async def get_chat_users(chat_id):
    users = []
    async for member in app.get_chat_members(chat_id):
        if member.user.is_bot or member.user.is_deleted:
            continue
        users.append(member.user)
    return users

async def tag_users(chat_id, messages, tag_type):
    users = await get_chat_users(chat_id)
    for i in range(0, len(users), 5):
        if chat_id not in active_chats:
            break
        batch = users[i:i+5]
        mentions = " ".join([f"[{u.first_name}](tg://user?id={u.id})" for u in batch])
        msg = random.choice(messages).format(mention=mentions)
        await app.send_message(chat_id, msg, disable_web_page_preview=True, parse_mode=enums.ParseMode.MARKDOWN)
        await asyncio.sleep(2)
    active_chats.pop(chat_id, None)
    await app.send_message(chat_id, f"✅ {tag_type} etiketleme tamamlandı!")

# ======= GÜNAYDIN KOMUTLARI =======
@app.on_message(filters.command("gtag") & filters.group)
async def gtag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ Günaydın etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("☀️ Günaydın etiketleme başlatıldı...")
    await tag_users(chat_id, GTAG_MESSAGES, "Günaydın")

@app.on_message(filters.command("gmstop") & filters.group)
async def gmtag_stop(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 Günaydın etiketleme durduruldu.")
    else:
        await message.reply("❌ Aktif bir etiketleme bulunamadı.")

# ======= İYİ GECELER KOMUTLARI (itag) =======
@app.on_message(filters.command("itag") & filters.group)
async def itag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ İyi geceler etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("🌙 İyi geceler etiketleme başlatıldı...")
    await tag_users(chat_id, ITAG_MESSAGES, "İyi Geceler")

@app.on_message(filters.command("istop") & filters.group)
async def itag_stop(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 İyi geceler etiketleme durduruldu.")
    else:
        await message.reply("❌ Aktif bir etiketleme bulunamadı.")

# ======= SOHBETE ÇAĞIRMA KOMUTLARI (stag) =======
@app.on_message(filters.command("stag") & filters.group)
async def stag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ Sohbete çağırma etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("💬 Sohbete çağırma etiketleme başlatıldı...")
    await tag_users(chat_id, STAG_MESSAGES, "Sohbete Çağırma")

@app.on_message(filters.command("ststop") & filters.group)
async def stag_stop(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 Sohbete çağırma etiketleme durduruldu.")
    else:
        await message.reply("❌ Aktif bir etiketleme bulunamadı.")

# ======= KURT OYUNU KOMUTLARI =======
@app.on_message(filters.command("ktag") & filters.group)
async def ktag(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        return await message.reply("⚠️ Kurt oyunu etiketleme zaten devam ediyor.")
    active_chats[chat_id] = True
    await message.reply("🐺 Kurt oyunu etiketleme başlatıldı...")
    await tag_users(chat_id, KTAG_MESSAGES, "Kurt Oyunu")

@app.on_message(filters.command("kstop") & filters.group)
async def ktag_stop(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 Kurt oyunu etiketleme durduruldu.")
    else:
        await message.reply("❌ Aktif bir etiketleme bulunamadı.")

# ======= GENEL KOMUTLAR =======
@app.on_message(filters.command("stopall") & filters.group)
async def stopall(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_chats:
        del active_chats[chat_id]
        await message.reply("🛑 Tüm etiketlemeler durduruldu.")
    else:
        await message.reply("❌ Aktif bir etiketleme bulunamadı.")

@app.on_message(filters.command("taghelp") & filters.group)
async def taghelp(_, message: Message):
    help_text = """
🏷️ **Etiketleme Komutları Yardımı**

**Günaydın:**
• `/gtag` - Günaydın etiketlemeyi başlatır  
• `/gmstop` - Günaydın etiketlemeyi durdurur

**İyi Geceler:**
• `/itag` - İyi geceler etiketlemeyi başlatır  
• `/istop` - İyi geceler etiketlemeyi durdurur

**Sohbete Çağırma:**
• `/stag` - Sohbete çağırma etiketlemeyi başlatır  
• `/ststop` - Sohbete çağırma etiketlemeyi durdurur

**Kurt Oyunu:**
• `/ktag` - Kurt oyunu etiketlemeyi başlatır  
• `/kstop` - Kurt oyunu etiketlemeyi durdurur

**Genel:**
• `/stopall` - Tüm aktif etiketlemeleri durdurur  
• `/taghelp` - Bu yardım mesajını gösterir

*Not:* Her sohbette aynı anda sadece bir etiketleme aktif olabilir.
"""
    await message.reply(help_text)
