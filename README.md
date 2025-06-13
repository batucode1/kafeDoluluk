# Kafe Doluluk Analizi API

Bu proje, kafe fotoğraflarını ChatGPT Vision API kullanarak analiz eden bir Flask uygulamasıdır.

## Özellikler

- Kafe fotoğraflarını analiz eder
- Doluluk oranını belirler
- Boş sandalye/masa sayısını sayar
- Kafe atmosferini değerlendirir
- RESTful API endpoint'i

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Environment variable ayarlayın:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

3. Uygulamayı çalıştırın:
```bash
python app.py
```

## API Kullanımı

### Kafe Analizi
**Endpoint:** `POST /analyze`

**Request:**
- Content-Type: `multipart/form-data`
- Body: `image` field'ında kafe fotoğrafı

**Response:**
```json
{
  "success": true,
  "result": "Bu kafe fotoğrafında...",
  "message": "Kafe analizi tamamlandı"
}
```

### Health Check
**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "message": "Kafe analiz API çalışıyor"
}
```

## Örnek Kullanım

```bash
curl -X POST -F "image=@kafe_foto.jpg" http://localhost:5000/analyze
```

## Güvenlik

- API key'i environment variable olarak saklayın
- Dosya türü kontrolü yapılır
- Geçici dosyalar otomatik temizlenir 