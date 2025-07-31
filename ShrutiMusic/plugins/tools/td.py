import json
import random
from pyrogram import filters
from ShrutiMusic import app

# JSON dosyasını yükle
try:
    with open("truth_or_dare.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    data = {"truth": [], "dare": []}
    print(f"[Truth or Dare] JSON yüklenirken hata oluştu: {e}")

# /d → Doğruluk
@app.on_message(filters.command("d"))
async def get_truth(client, message):
    try:
        truth_list = data.get("truth", [])
        if truth_list:
            question = random.choice(truth_list)
            await message.reply_text(f"🟢 Doğruluk Sorusu:\n\n{question}")
        else:
            await message.reply_text("⚠️ Herhangi bir doğruluk sorusu bulunamadı.")
    except Exception:
        await message.reply_text("❌ Bir hata oluştu. Lütfen tekrar deneyin.")

# /c → Cesaret
@app.on_message(filters.command("c"))
async def get_dare(client, message):
    try:
        dare_list = data.get("dare", [])
        if dare_list:
            question = random.choice(dare_list)
            await message.reply_text(f"🔴 Cesaret Görevi:\n\n{question}")
        else:
            await message.reply_text("⚠️ Herhangi bir cesaret görevi bulunamadı.")
    except Exception:
        await message.reply_text("❌ Bir hata oluştu. Lütfen tekrar deneyin.")

# Yardım mesajı
__HELP__ = """
**D / C Oyunu 🎲 - Doğruluk mu Cesaret mi?**

🎯 Komutlar:
- `/d` → Rastgele bir *doğruluk sorusu* al
- `/c` → Rastgele bir *cesaret görevi* al

🧠 Örnekler:
- `/d`: "Hiç kimseye söylemediğin bir sırrın var mı?"
- `/c`: "30 saniye boyunca komik bir şekilde dans et"

Sorular sabit dosyadan rastgele çekilir. Eğlenceye hemen başla!
"""

__MODULE__ = "D / C Oyunu"
