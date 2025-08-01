import random
import json
import os
import asyncio
from datetime import datetime, timedelta
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ShrutiMusic import app  # Mevcut Pyrogram Client örneğin

SIIR_JSON = os.path.join(os.path.dirname(__file__), "siirler.json")
SUDO_JSON = os.path.join(os.path.dirname(__file__), "sudo_users.json")
KANAL_USERNAME = "tubidymusic"
OWNER_IDS = [6289700114, 7426116391]

def load_json(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_siirler():
    return load_json(SIIR_JSON)

def save_siirler(siirler):
    save_json(SIIR_JSON, siirler)

def add_siir(yeni_siir, yazar):
    siirler = load_siirler()
    siirler.append({"text": yeni_siir, "author": yazar})
    save_siirler(siirler)

def load_sudo_users():
    data = load_json(SUDO_JSON)
    for owner in OWNER_IDS:
        if owner not in data:
            data.append(owner)
    return data

def save_sudo_users(data):
    save_json(SUDO_JSON, data)

def siir_footer():
    return f"\n\n—\n🖋 @{KANAL_USERNAME}"

@app.on_message(filters.command(["sudoadd"]) & filters.user(OWNER_IDS))
async def sudoadd_handler(client: Client, message: Message):
    args = message.text.split()
    if len(args) != 2:
        await message.reply("Kullanım: /sudoadd <kullanıcı_id>")
        return

    try:
        new_id = int(args[1])
    except ValueError:
        await message.reply("Geçerli bir kullanıcı ID'si girin.")
        return

    sudo_users = load_sudo_users()
    if new_id in sudo_users:
        await message.reply("Bu kullanıcı zaten yetkili.")
        return

    sudo_users.append(new_id)
    save_sudo_users(sudo_users)
    await message.reply(f"✅ Kullanıcı ID `{new_id}` yetkililere eklendi.")

@app.on_message(filters.command(["sudoadd"]))
async def sudoadd_unauthorized(client: Client, message: Message):
    if message.from_user.id not in OWNER_IDS:
        await message.reply("❌ Üzgünüm, gerekli yetkilere sahip değilsiniz.")

@app.on_message(filters.command(["şiiradd", ".şiiradd"]))
async def siir_ekle(client: Client, message: Message):
    sudo_users = load_sudo_users()
    user_id = message.from_user.id

    if user_id not in sudo_users:
        await message.reply("❌ Üzgünüm, gerekli yetkilere sahip değilsiniz.")
        return

    args = message.text.split(None, 1)
    if len(args) < 2:
        await message.reply("❌ Şiiri komuttan sonra yazmalısınız. Örnek:\n/şiiradd Gönül ne kahramanlıklar gördü...")
        return

    yeni_siir = args[1].strip()
    if len(yeni_siir) < 10:
        await message.reply("❌ Çok kısa şiir kabul edilmiyor.")
        return

    yazar = message.from_user.username or message.from_user.first_name or "Anonim"
    add_siir(yeni_siir, yazar)
    await message.reply("✅ Şiir başarıyla eklendi!")

@app.on_message(filters.command(["şiir", ".şiir"]) & (filters.group | filters.private))
async def siir_gonder(client: Client, message: Message):
    siirler = load_siirler()
    if not siirler:
        await message.reply("❌ Henüz kayıtlı şiir yok.")
        return

    secilen = random.choice(siirler)
    siir_metni = secilen["text"]
    siir_yazar = secilen.get("author", "Anonim")

    text = f"{siir_metni}\n\n—\n✍️ {siir_yazar}{siir_footer()}"
    await message.reply(text, parse_mode=enums.ParseMode.MARKDOWN)

class SiirOylama:
    def __init__(self):
        self.active_votes = {}
        self.vote_duration = timedelta(hours=24)  # 24 saat

    async def start_vote(self):
        siirler = load_siirler()
        if not siirler:
            return

        siir = random.choice(siirler)
        siir_text = siir["text"]
        siir_author = siir.get("author", "Anonim")

        # Bot'un yetkili olduğu grupların ID'lerini al
        yetkili_gruplar = []
        for dialog in await app.get_dialogs():
            if dialog.chat.type in ("group", "supergroup"):
                try:
                    member = await app.get_chat_member(dialog.chat.id, app.me.id)
                    if member.status in ("administrator", "creator"):
                        yetkili_gruplar.append(dialog.chat.id)
                except:
                    continue

        for gid in yetkili_gruplar:
            end_time = datetime.now() + self.vote_duration
            self.active_votes[gid] = {
                "siir": siir,
                "yes": set(),
                "no": set(),
                "end_time": end_time
            }

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("👍 Evet", callback_data=f"vote_yes_{gid}"),
                        InlineKeyboardButton("👎 Hayır", callback_data=f"vote_no_{gid}")
                    ]
                ]
            )

            await app.send_message(
                gid,
                f"📜 Günün Şiiri:\n\n{siir_text}\n\n—\n✍️ {siir_author}{siir_footer()}\n\nBeğendiniz mi?",
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.MARKDOWN
            )

    async def check_votes(self):
        now = datetime.now()
        for gid, vote in list(self.active_votes.items()):
            if now >= vote["end_time"]:
                yes_count = len(vote["yes"])
                no_count = len(vote["no"])
                siir = vote["siir"]
                siir_text = siir["text"]
                siir_author = siir.get("author", "Anonim")

                total = yes_count + no_count
                if total > 0 and yes_count / total >= 0.5:
                    await app.send_message(
                        KANAL_USERNAME,
                        f"🎉 Yeni onaylı şiir:\n\n{siir_text}\n\n—\n✍️ {siir_author}{siir_footer()}",
                        parse_mode=enums.ParseMode.MARKDOWN
                    )
                del self.active_votes[gid]

@app.on_callback_query()
async def vote_callback(client, callback_query):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data.startswith("vote_yes_") or data.startswith("vote_no_"):
        gid = int(data.split("_")[-1])
        if gid not in siir_oylama.active_votes:
            await callback_query.answer("Oylama sona ermiş.")
            return

        vote = siir_oylama.active_votes[gid]
        if user_id in vote["yes"] or user_id in vote["no"]:
            await callback_query.answer("Zaten oy kullandınız!")
            return

        if data.startswith("vote_yes_"):
            vote["yes"].add(user_id)
            await callback_query.answer("Evet oyunu kullandınız.")
        else:
            vote["no"].add(user_id)
            await callback_query.answer("Hayır oyunu kullandınız.")

siir_oylama = SiirOylama()

async def scheduler():
    while True:
        await siir_oylama.start_vote()
        await asyncio.sleep(24 * 3600)  # 24 saatte bir

asyncio.get_event_loop().create_task(scheduler())

if __name__ == "__main__":
    app.run()

__MODULE__ = "Gᴀʟɪ"
__HELP__ = """
**Şiir Komutları**

- /şiir - Rastgele şiir gönderir
- /şiiradd - Şiir ekleme komutu (sadece yetkililer)
- /sudoadd - Yetkili ekleme komutu (sadece Ownerlar)
"""
