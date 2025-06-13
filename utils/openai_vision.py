# -*- coding: utf-8 -*-
import openai
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# API key'i environment variable'dan oku
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Yeni OpenAI istemcisini başlat
client = openai.OpenAI(api_key=api_key)

def analyze_image_with_gpt(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "Bu kafe fotoğrafını analiz et ve sadece kısa net ve sayısal cevaplar ver. Şu bilgileri ver: 1. Kafe ne kadar dolu? (boş, az dolu, orta dolu, çok dolu)2. Kaç kişi oturuyor?3. Kaç boş sandalye/masa var? 4. Genel olarak ne kadar yer var? 5. Kafe atmosferi nasıl? (sakin, kalabalık, vs.) 6. Sonuç olarak oturulabilecek kaç masa ve sandalye var, kafe ne derece müsait?(3 masa 10 sandalye var, kafe orta derecede müsait vs) "},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content
