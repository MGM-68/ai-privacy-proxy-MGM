
import urllib.request
import json

url = "http://localhost:11434/api/generate"

# 1. Наш секретный исходный текст
original_text = "Сегодня Maria Rossi подписала конфиденциальный контракт с Dell на сумму 45000 евро."

# 2. Умный промпт: просим Ламу вернуть не просто текст, а структуру JSON
prompt = f"""
Ты - строгий GDPR-цензор. Твоя задача найти в тексте персональные и корпоративные данные (имена, названия компаний, суммы) и заменить их на безопасные теги: [PERSON_1], [COMPANY_1], [AMOUNT_1].

ВАЖНО: Верни ответ строго в формате JSON, содержащий ровно два поля:
1. "anonymized_text" - готовый текст с тегами.
2. "dictionary" - словарь, где ключи - это теги, а значения - оригинальные слова, которые ты скрыл.

Текст для обработки: {original_text}
"""

data = {
    "model": "llama3.1:latest",
    "prompt": prompt,
    "stream": False,
    "format": "json" # Жестко заставляем модель отвечать в формате JSON
}

req_data = json.dumps(data).encode("utf-8")
req = urllib.request.Request(url, data=req_data, headers={"Content-Type": "application/json"})

print("Отправляем запрос локальной Ламе, ждем...")

try:
    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        result = json.loads(response_body)
        
        # Лама присылает нам JSON-строку, превращаем её в настоящий словарь Python
        llama_reply = json.loads(result["response"])
        
        print("\n--- ☁️ ТЕКСТ ДЛЯ ОБЛАКА (Анонимный) ---")
        print(llama_reply["anonymized_text"])
        
        print("\n--- 🔒 НАШ СЕКРЕТНЫЙ СЛОВАРЬ (Остается на ПК) ---")
        print(llama_reply["dictionary"])

except Exception as e:
    print("\nОшибка соединения с Ламой:", e)