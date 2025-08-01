import asyncio
import random
from pyrogram import filters
from pyrogram.types import Message
from pyrogram import enums
from ShrutiMusic import app

active_chats = {}

# gtag - Günaydın Etiketleri (50 adet)
GTAG_MESSAGES = [
    "🌞 {mention}, uyan artık! Güneşi sen mi bekliyorsun?",
    "☕ Kahveni hazırla, {mention}, çünkü bugün harika geçecek!",
    "🐓 {mention}, horoz bile seni geçti, hadi kalk!",
    "🌅 Yeni güne merhaba de, {mention}!",
    "📢 Alarm çaldı, uyanma vakti {mention}!",
    "🍳 Kahvaltı sofrası seni bekliyor, {mention}!",
    "🌈 Güne pozitif başla, {mention}!",
    "🌻 Gülümse, hayat güzel, {mention}!",
    "🦄 Bugün mucizeler günü, kaçırma {mention}!",
    "🎉 Günaydın {mention}, enerji sende mi?",
    "🛌 Uykunun sonu geldi {mention}, artık kalk!",
    "🎵 Güne güzel bir melodiyle başla, {mention}!",
    "🦋 Hayat kısa, kahveni al ve gülümse {mention}!",
    "🌞 Güneş doğdu, sen nerdesin {mention}?",
    "🥐 Kahvaltı hazırsa, haydi {mention}!",
    "🚀 Bugün yıldız gibi parlamaya hazır mısın {mention}?",
    "🥳 Güne neşe kat, {mention}!",
    "📅 Yeni bir gün, yeni fırsatlar, {mention}!",
    "🌸 Bahar geldi, uyan {mention}!",
    "☀️ Enerjini topla, {mention}!",
    "🍯 Tatlı bir gün olsun {mention}!",
    "🐝 Uyan ve üret, {mention}!",
    "🌤️ Gökyüzü senin için parlıyor, {mention}!",
    "🏞️ Doğa seni çağırıyor, kalk {mention}!",
    "🎨 Bugün hayatını renklendir, {mention}!",
    "💪 Güç sende, uyan {mention}!",
    "📖 Yeni bir sayfa aç, {mention}!",
    "🌷 Günaydın, {mention}, taze bir başlangıç!",
    "🦚 Bugün kendine iyi bak, {mention}!",
    "🍓 Tatlı anlar seni bekliyor, {mention}!",
    "🕊️ Huzurla uyan {mention}!",
    "☁️ Bulutların üstünde hisset kendini, {mention}!",
    "🎯 Hedeflerine odaklan, {mention}!",
    "🍃 Derin nefes al, {mention}!",
    "🥰 Gülümse, dünya daha güzel seninle {mention}!",
    "🌟 Bugün parlamaya hazırsın, {mention}!",
    "📢 Sesin duyulsun, {mention}!",
    "🌼 Sabah çiçekleri gibi aç {mention}!",
    "🧩 Her şey yerli yerinde, sadece kalk {mention}!",
    "🍋 Limonata gibi taze başla, {mention}!",
    "🌙 Gece bitti, gündüz başladı {mention}!",
    "🐣 Yeni bir başlangıç seni bekliyor, {mention}!",
    "🍂 Sonbahar rüzgarı gibi hafif uyan, {mention}!",
    "🎈 Hayat kısa, bugün başla {mention}!",
    "🦄 Hayal et ve gerçekleştir, {mention}!",
    "🌺 Yeni umutlarla dolu bir gün {mention}!",
    "🎇 Enerjinle etrafını aydınlat {mention}!",
    "🥁 Ritmini yakala, {mention}!",
    "🌳 Kendine zaman ayır, {mention}!",
    "🌞 Güne pozitif başla, {mention}!"
]

# itag - İyi Geceler Etiketleri (50 adet)
ITAG_MESSAGES = [
    "🌙 {mention}, gözlerini kapat ve güzel rüyalar gör!",
    "🛌 Uykunun kollarına bırak kendini {mention}!",
    "😴 Haydi uyu {mention}, sabah yine gelecek!",
    "🌌 Yıldızlar seni korusun, {mention}!",
    "🕯️ Mum ışığında huzur dolu bir gece {mention}!",
    "🐑 Koyun saymayı bırak, uyu {mention}!",
    "🌠 Rüyanda en güzel maceraları yaşa {mention}!",
    "🎭 Hayallerin sahnesi seni bekliyor, {mention}!",
    "💤 Tatlı uykular {mention}!",
    "📵 Telefonu kapat, dinlen {mention}!",
    "🌺 Gece çiçekleri gibi huzurlu uyu {mention}!",
    "🦉 Geceyi kuşlar gibi sessiz geçir {mention}!",
    "🛸 Rüyanda uzay yolculuğu yap {mention}!",
    "🎇 Geceyi yıldızlarla süsle {mention}!",
    "💫 Hayal gücünü serbest bırak {mention}!",
    "🌜 Ay ışığı gibi sakin uyu {mention}!",
    "🌹 Tatlı rüyalarla dolu olsun gecen {mention}!",
    "🔥 Ateş böcekleri kadar parlak uyu {mention}!",
    "🎶 Ninni gibi huzurlu uyu {mention}!",
    "🌃 Gece sana iyi gelsin {mention}!",
    "🌟 Yıldızlar seninle parlasın {mention}!",
    "🦋 Rüyaların kelebekler gibi hafif olsun {mention}!",
    "🍵 Sıcak bir çay eşliğinde uyu {mention}!",
    "🛏️ Rahat bir uyku çek {mention}!",
    "💤 Uykunun tadını çıkar {mention}!",
    "🌙 Huzurla dolu geceler {mention}!",
    "🦇 Karanlıkta kaybolma, iyi uyu {mention}!",
    "🌌 Evren seninle {mention}!",
    "🛡️ Rüyalarında korun {mention}!",
    "🌠 Gökyüzüne uzan, güzel uyu {mention}!",
    "🦉 Gecenin bilgeliği seninle olsun {mention}!",
    "🎇 Uykun ışık saçsın {mention}!",
    "🌜 Hayallerin gerçek olsun {mention}!",
    "🎵 Uyku melodisi eşlik etsin {mention}!",
    "🦄 Rüyanda sihir olsun {mention}!",
    "🌷 Gece bahçesinde yürüyüş yap {mention}!",
    "💤 Sakin ve derin uyu {mention}!",
    "🌺 Tatlı rüyalarla uyan {mention}!",
    "🌙 Yıldız tozları düşsün rüyana {mention}!",
    "🍂 Sonbahar yaprakları gibi huzurlu uyu {mention}!",
    "🛌 Günün stresini unut, uyu {mention}!",
    "💫 Rüyanda parılda {mention}!",
    "🦉 Gece senin arkadaşın {mention}!",
    "🌌 Uykun evrene yayılsın {mention}!",
    "🕯️ Huzurlu uyku seni sarsın {mention}!",
    "🎇 Geceyi kutla, uyu {mention}!",
    "💤 Rüyaların en tatlısı olsun {mention}!",
    "🌙 Tatlı düşler gör {mention}!",
    "🛏️ Uykunun krallığına hoş geldin {mention}!"
]

# stag - Sohbete Çağırma Etiketleri (50 adet)
STAG_MESSAGES = [
    "🎉 Hey {mention}, sohbet başlıyor, gel katıl!",
    "📢 {mention}, sessiz kalma, buradayız!",
    "🔥 {mention}, seni bekliyoruz, hadi gel!",
    "💬 Sohbet ateşi yanıyor, {mention}!",
    "🎊 Eğlence başlasın, {mention} buraya!",
    "🚀 {mention}, sohbet gemisi kalkıyor!",
    "🎈 {mention}, muhabbet zamanı!",
    "📣 Sesini duyur, {mention}!",
    "🌟 Sen olmadan eksik kalırız {mention}!",
    "💥 Hadi bakalım {mention}, sohbet zamanı!",
    "🎤 Mikrofon sende, {mention}!",
    "🕺 Dans etmeye gerek yok, sadece konuş {mention}!",
    "🍿 Sohbet patlaması için hazır ol {mention}!",
    "🎮 Oyun bitti, şimdi muhabbet vakti {mention}!",
    "💌 Sohbet daveti, {mention}!",
    "🎭 Rolünü al, {mention}, konuşma zamanı!",
    "📚 Hikayelerini paylaş, {mention}!",
    "🎉 Parti burada, katıl {mention}!",
    "🌈 Renkli sohbetlere gel {mention}!",
    "🎬 Sohbet filmi başladı, {mention}!",
    "🎯 Hedef: Muhabbet, {mention}!",
    "🥳 Bugün senin günün, gel {mention}!",
    "🗣️ Söyleyeceklerin var mı {mention}?",
    "🎶 Sohbetin ritmini yakala {mention}!",
    "🦄 Sıradışı konuşmalar için buradayız {mention}!",
    "🌞 Günün en güzel sohbeti seni bekliyor {mention}!",
    "🌻 Enerjini kat, {mention}!",
    "🛎️ Zil çaldı, muhabbet başladı {mention}!",
    "🌍 Dünya durdu, sohbet başladı {mention}!",
    "🧩 Eksik parçamsın, gel {mention}!",
    "🎉 Kutlama zamanı, muhabbet seni çağırıyor {mention}!",
    "🔥 Ateşi yak, {mention}!",
    "🎤 Söz sende, {mention}!",
    "💥 Muhabbet bombası, patlat {mention}!",
    "🍰 Tatlı sözler için buradayız {mention}!",
    "🥂 Sohbet kadehi kaldırıldı, gel {mention}!",
    "🎯 Hadi odaklan, {mention}!",
    "💫 Muhabbet yıldızı ol {mention}!",
    "🎭 Maskeni çıkar, gerçek sen ol {mention}!",
    "🎉 Eğlence başlasın, {mention}!",
    "🌟 Parla, ışılda {mention}!",
    "📢 Sesin çok önemli, duyur {mention}!",
    "🌈 Muhabbet gökkuşağına katıl {mention}!",
    "🚀 Sohbet roketi kalkıyor {mention}!",
    "🦄 Sen olunca her şey daha güzel {mention}!",
    "🎤 Konuşma mikrofonu senin, {mention}!",
    "🎉 Hadi şimdi senin zamanın, {mention}!",
    "🎯 Muhabbet hedefi: {mention}!",
    "🥳 Bugün senin günü, gel {mention}!",
    "🎶 Ritim senin, sohbet senin {mention}!",
    "🔥 Ateşi yak, muhabbeti başlat {mention}!"
]

# ktag - Kurt Oyununa Çağırma Etiketleri (50 adet)
KTAG_MESSAGES = [
    "🐺 {mention}, kurtlar geceyi bekliyor, gel!",
    "🌕 Ay doldu, kurtlar uluyor, sen neredesin {mention}?",
    "🔥 Kamp ateşi yanıyor, kurtlar seni çağırıyor {mention}!",
    "🎲 Oyun başlasın, kurt takımına katıl {mention}!",
    "🕵️‍♂️ Gizemli geceye hazır mısın {mention}?",
    "🌌 Yıldızlar altında kurtlarla oyna {mention}!",
    "⚔️ Kurtlar savaşı başlıyor, sen de katıl {mention}!",
    "🎯 Hedef: Kurt olmak, hazır mısın {mention}?",
    "🎭 Rolünü seç, kurt ol ya da kurtlan {mention}!",
    "🗡️ Silahlarını kuşan, oyun başlıyor {mention}!",
    "🐾 Ayak izlerin takipte, dikkat et {mention}!",
    "🌲 Ormanın derinlikleri seni bekliyor {mention}!",
    "🌙 Gece kurtlarındır, sen de katıl {mention}!",
    "🎉 Kurt partisi başladı, gel {mention}!",
    "🔥 Ateşi harla, takımını kur {mention}!",
    "🚨 Alarm ver, kurtlar toplanıyor {mention}!",
    "🎤 Kurt uluması zamanı, ses ver {mention}!",
    "🦴 Kemiklerinizi hazırla, oyun başlıyor {mention}!",
    "🕶️ Gizemli kurt, sen neredesin {mention}?",
    "🌑 Gece karanlık, kurtlar cesur {mention}!",
    "🏞️ Ormanda macera seni bekliyor {mention}!",
    "🧩 Bulmacaları çöz, kurt takımını kurtar {mention}!",
    "🎲 Zar at, kaderin kurt ol {mention}!",
    "⚡ Gücünü göster, kurt takımına katıl {mention}!",
    "🌟 Yıldızlar altında takım ol {mention}!",
    "🐕 Sadık kurtlara katıl {mention}!",
    "🔥 Ateş çevresinde plan yap {mention}!",
    "🎯 Doğru kararı ver, kurt kazanır {mention}!",
    "🕵️ Gizli kurtlar aramızda {mention}!",
    "🌜 Geceyi fethet, kurt sen ol {mention}!",
    "🛡️ Koruma zamanın geldi {mention}!",
    "🎉 Eğlence kurtlarla {mention}!",
    "⚔️ Savaş zamanı, takımını kur {mention}!",
    "🎲 Şansını dene, kurt ol {mention}!",
    "🌲 Orman bekliyor, macera seni çağırıyor {mention}!",
    "🐺 Uluma zamanı, sesi duyur {mention}!",
    "🔥 Ateşi yak, takımını topla {mention}!",
    "🕶️ Kurt kılığına gir {mention}!",
    "🌙 Ay ışığında buluşalım {mention}!",
    "🎯 Hedef belirle, oyunu kazan {mention}!",
    "🦴 Kemiklere sahip çık {mention}!",
    "🛡️ Kalkanını hazırla, takımını savun {mention}!",
    "🎤 Uluma sesi gönder {mention}!",
    "🌟 Yıldızlı gece senin için {mention}!",
    "🎲 Oyun zarları atıldı {mention}!",
    "🔥 Ateş başında plan yap {mention}!",
    "🐾 İzini bırak, iz sürücü ol {mention}!",
    "⚡ Hızlı ol, kurtlar kazanır {mention}!",
    "🎭 Maskeni tak, rolüne bürün {mention}!",
    "🌌 Gece boyunca takım ol {mention}!",
    "🎉 Kutlama zamanı geldi {mention}!",
    "🐺 Kurtlar gecesi başladı {mention}!"
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
    total_users = len(users)
    tagged_count = 0

    for user in users:
        if chat_id not in active_chats or active_chats[chat_id]["type"] != tag_type:
            break
        
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        msg = random.choice(messages).format(mention=mention)
        
        await app.send_message(chat_id, msg, disable_web_page_preview=True, parse_mode=enums.ParseMode.MARKDOWN)
        
        tagged_count += 1
        active_chats[chat_id]["users_tagged"] = tagged_count
        
        await asyncio.sleep(4)
        
    active_chats.pop(chat_id, None)

    await app.send_message(
        chat_id,
        f"✅ {tag_type} etiketleme tamamlandı!\n\n"
        f"👥 Toplam üye sayısı: {total_users}\n"
        f"🏷️ Etiketlenen üye sayısı: {tagged_count}"
    )

def is_active_tagging(chat_id):
    return chat_id in active_chats

def active_tag_type(chat_id):
    return active_chats[chat_id]["type"] if chat_id in active_chats else None

# Komutlar:

@app.on_message(filters.command("gtag") & filters.group)
async def gtag(_, message: Message):
    chat_id = message.chat.id
    if is_active_tagging(chat_id):
        return await message.reply(f"⚠️ Başka bir etiketleme zaten aktif: `{active_tag_type(chat_id)}`.")
    active_chats[chat_id] = {"type": "Günaydın", "users_tagged": 0}
    await message.reply("☀️ Günaydın etiketleme başlatıldı...")
    await tag_users(chat_id, GM_MESSAGES, "Günaydın")

@app.on_message(filters.command("itag") & filters.group)
async def itag(_, message: Message):
    chat_id = message.chat.id
    if is_active_tagging(chat_id):
        return await message.reply(f"⚠️ Başka bir etiketleme zaten aktif: `{active_tag_type(chat_id)}`.")
    active_chats[chat_id] = {"type": "İyi Geceler", "users_tagged": 0}
    await message.reply("🌙 İyi geceler etiketleme başlatıldı...")
    await tag_users(chat_id, GN_MESSAGES, "İyi Geceler")

@app.on_message(filters.command("stag") & filters.group)
async def stag(_, message: Message):
    chat_id = message.chat.id
    if is_active_tagging(chat_id):
        return await message.reply(f"⚠️ Başka bir etiketleme zaten aktif: `{active_tag_type(chat_id)}`.")
    active_chats[chat_id] = {"type": "Sohbete Çağırma", "users_tagged": 0}
    await message.reply("📢 Sohbete çağırma etiketleme başlatıldı...")
    await tag_users(chat_id, STAG_MESSAGES, "Sohbete Çağırma")

@app.on_message(filters.command("ktag") & filters.group)
async def ktag(_, message: Message):
    chat_id = message.chat.id
    if is_active_tagging(chat_id):
        return await message.reply(f"⚠️ Başka bir etiketleme zaten aktif: `{active_tag_type(chat_id)}`.")
    active_chats[chat_id] = {"type": "Kurt Oyunu", "users_tagged": 0}
    await message.reply("🐺 Kurt oyunu etiketleme başlatıldı...")
    await tag_users(chat_id, KTAG_MESSAGES, "Kurt Oyunu")

# Durdurma komutları
@app.on_message(filters.command(["dur", "durdur", "iptal", "cancel"]) & filters.group)
async def stop_tagging(_, message: Message):
    chat_id = message.chat.id
    if is_active_tagging(chat_id):
        etiket_turu = active_tag_type(chat_id)
        del active_chats[chat_id]
        await message.reply(f"🛑 {etiket_turu} etiketleme durduruldu.")
    else:
        await message.reply("❌ Aktif bir etiketleme bulunamadı.")

# Yardım komutu
@app.on_message(filters.command("etiketyardim") & filters.group)
async def taghelp(_, message: Message):
    help_text = """
🏷️ **Etiketleme Komutları**

• `/gtag` - Günaydın etiketlemeyi başlatır  
• `/itag` - İyi geceler etiketlemeyi başlatır  
• `/stag` - Sohbete çağırma mesajları ile etiketler  
• `/ktag` - Kurt oyununa çağırma mesajları ile etiketler  

• `/dur` veya `/durdur` veya `/iptal` veya `/cancel` - Aktif etiketlemeyi durdurur  
• `/etiketyardim` - Bu yardım mesajını gösterir  

**Not:** Aynı anda sadece bir etiketleme aktif olabilir.
"""
    await message.reply(help_text)
