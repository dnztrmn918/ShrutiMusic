import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message

# Burada kendi bot token'ınızı ayarlayın veya config dosyasından çekin
# Örnek: app = Client("my_bot", bot_token="TOKENINIZ")
app = Client("my_bot")

DOKUNDURMA_MESAJLARI = [
    "Yine mi karıştın işlere, {mention}? Beyin nerede kayıp acaba? 🤔",
    "Akıl fukaralığı sınırları zorluyorsun {mention}, Nobel de bekliyoruz! 😂",
    "Seninle uğraşmak ayrı sabır işi, adam gibi ol biraz {mention}!",
    "Konuşma hızını yavaşlat da, böyle deli gibi söyleyip kimse anlamasın {mention}!",
    "Seninle sohbet etmek, dalgıçlık kursuna gitmek gibi; derin ve zor {mention}!",
    "Kafanı toparla biraz da dünya senin etrafında dönmüyor {mention}!",
    "Çok konuşup az iş yapanlar kulübüne hoş geldin {mention}!",
    "Gülme sesin kadar zekan da eksik galiba {mention}, en azından sessiz ol!",
    "Bu kadar takılma, rahatla biraz, yoksa dişçiye gitmen gerekebilir {mention}!",
    "Aman dikkat et, ciddiye alınmak için biraz değişmen lazım {mention}!",
    "Sen olmasan grup ne sıkıcı olurdu, devam et komedi yapmaya {mention}!",
    "Biraz sakin ol da biz de nefes alalım, azıcık mı rahatla {mention}!",
    "Kendini fazla kaptırma, hayat bu kadar da abartılmaz {mention}!",
    "Bugün biraz daha sessiz kal da kulaklarımız şenlensin {mention}!",
    "Takılma huyunu bırak, hayat kısa senin kadar uzun değil {mention}!",
    "Seninle uğraşmak terapi gibi geliyor, devam et biraz {mention}!",
    "Dur bakalım, biraz toparlan da biz de dinlenelim, zor sabrediyoruz {mention}!",
    "Yine mi sen? Vay be, sen olmasan bu grup boş kalırdı {mention}!",
    "Hadi bakalım, biraz da biz konuşalım da sen dinle {mention}!",
    "Efsanesin ama biraz yavaşla, her şeyin bir sınırı var {mention}!",
    "Nefes almayı unutma, bazen mola vermek lazım, yoksa patlarsın {mention}!",
    "O kadar konuşma, kulaklarım yoruldu, biraz susmayı dene {mention}!",
    "Şaka mı yapıyorsun, yoksa ciddi misin? Zor anlaşılan bir haldesin {mention}!",
    "Bazen susmak da altın değerindedir, sen denemelisin {mention}!",
    "Biraz düşün, sonra konuş, beyin yorgunluğu var galiba {mention}!",
    "Söz uçar, yazı kalır ama sen fark etmezsin, sen yazı okumayı dene {mention}!",
    "Dalgın mısın, yoksa sadece böyle mi davranıyorsun, karıştım {mention}!",
    "Biraz akıl, biraz saygı lazım sana, ütopik gelebilir ama dene {mention}!",
    "Dünyayı kurtarmaya çalışıyorsun ama kendini unutuyorsun, biraz sakin ol {mention}!",
    "Seninle konuşmak bulmaca çözmek gibi, şifreyi çözmek lazım {mention}!",
    "Kendini fazla önemseme, etrafında sadece sen yoksun {mention}!",
    "Sen hayatı fazlasıyla ciddiye alıyorsun, biz de ciddiyetsiziz, bu dengeyi kur {mention}!",
    "Sen olmasan bu kadar eğlenceli olmazdı, biraz absürt insan {mention}!",
    "Sana ‘yavaşla’ demek, koşan adama ‘otur’ demek gibi, zor iş {mention}!",
    "Sen ne kadar konuşsan da biz seni hep aynı yere koyarız, değişmez {mention}!",
    "Kafanı çalıştırmayı dene, Google’a danışmadan önce {mention}!",
    "Mizah anlayışın 90'larda kalmış, güncellemeni öneririm {mention}!",
    "Sadece çok konuşma değil, azıcık anlamaya çalış da faydan olsun {mention}!",
    "O kadar hızlı konuşuyorsun ki, çevirmen lazım bize {mention}!",
    "Sözlerin bitse de suskunluğun konuşsa keşke {mention}!",
    "Kafanı topla da biz de seni ciddiye alalım biraz {mention}!",
    "Çok konuşman seni önemli yapmaz, aksine anlamazlar seni {mention}!",
    "Zeka pırıltısı yok ama ışık saçıyorsun, karanlıkları aydınlatıyorsun {mention}!",
    "Bazen sessizlik en iyi cevaptır, dene bakalım {mention}!",
    "Seninle muhabbet etmek zorlu ama eğlenceli bir macera {mention}!",
    "Kafanı dinle, kalbini dinle, biz seni bekleriz {mention}!",
    "Konuşmadan önce düşün, sonra pişman olma {mention}!",
    "Herkesin sevdiği 'karışık' tip sensin, şaşırmıyoruz {mention}!",
    "Yine mi sen? İyi ki varsın, yoksa sıkılırdık {mention}!",
    "Sabır taşı bizde çatladı, sen daha dayan biz de dayanırız {mention}!"
]

@app.on_message(
    filters.command(["dokundur", ".dokundur"], prefixes=["/", "."]) & filters.private
)
async def dokundur_private(client: Client, message: Message):
    mention = message.from_user.mention if message.from_user else "Kullanıcı"
    await message.reply_text(
        text=random.choice(DOKUNDURMA_MESAJLARI).format(mention=mention),
    )

@app.on_message(filters.command(["dokundur", ".dokundur"]) & filters.group)
async def dokundur_group(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    try:
        member = await client.get_chat_member(chat_id, user_id)
    except Exception:
        return
    
    if member.status in ["administrator", "creator"]:
        mention = message.reply_to_message.from_user.mention if message.reply_to_message else ""
        if mention:
            reply_msg = await message.reply(f"{mention} {random.choice(DOKUNDURMA_MESAJLARI).format(mention=mention)}")
        else:
            mention = message.from_user.mention if message.from_user else "Yönetici"
            reply_msg = await message.reply(random.choice(DOKUNDURMA_MESAJLARI).format(mention=mention))
        
        await asyncio.sleep(60)
        try:
            await reply_msg.delete()
            await message.delete()
        except Exception:
            pass
    else:
        reply_msg = await message.reply(
            "**🚫 Bu komut sadece yöneticiler içindir!**\n\n💬 Bu komutu özel mesajlarda deneyin."
        )
        await asyncio.sleep(10)
        try:
            await reply_msg.delete()
        except Exception:
            pass

if __name__ == "__main__":
    app.run()

__MODULE__ = "Dokundurma"
__HELP__ = """
**Dokundurma Komutu**

Bu komut özel mesajlarda rastgele sert ve esprili dokundurma mesajları sağlar.  
Gruplarda ise yalnızca adminler kullanabilir.  

Özellikler:  
- Botun DM'sinde herkes kullanabilir  
- Gruplarda sadece adminler/kurucular kullanabilir  
- Mesajlar gruplarda 1 dakika sonra otomatik silinir  
- /dokundur ve .dokundur komutlarını destekler  

Komutlar:  
- /dokundur - Rastgele dokundurma mesajı gönder (DM'de çalışır)  
- .dokundur - Alternatif komut formatı  
"""
