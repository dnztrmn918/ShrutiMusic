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


import os
import json
import random
from pyrogram import filters
from ShrutiMusic import app


# td.py dosyasının bulunduğu klasörün tam yolu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# JSON dosyasının tam yolu
json_path = os.path.join(BASE_DIR, "truth_or_dare.json")

# JSON verisini yükle
try:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print(f"JSON dosyası okunurken hata: {e}")
    data = {"truth": [], "dare": []}


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


__HELP__ = """
**Tʀᴜᴛʜ ᴏʀ ᴅᴀʀᴇ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs**

- `/d`: Rastgele bir doğruluk sorusu al.
- `/c`: Rastgele bir cesaret görevi al.

Sorular ve görevler `truth_or_dare.json` dosyasından yüklenmektedir.
"""

__MODULE__ = "Tʀᴜᴛʜ ᴏʀ ᴅᴀʀᴇ"
