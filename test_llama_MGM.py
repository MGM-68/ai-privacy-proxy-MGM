import urllib.request
import json

# Адрес нашего локального сервера Ollama
url = "http://localhost:11434/api/generate"

# Данные, которые мы отправляем модели
# (замени "llama3.1:latest" на то имя модели, которое ты скачала в Ollama, например "mistral" или "phi3")
# Данные, которые мы отправляем модели
data = {
    "model": "llama3.1:latest",
    "prompt": """Ты — строгий GDPR-цензор. Твоя задача: найти в тексте персональные и корпоративные данные (имена, названия компаний, суммы) и заменить их на безопасные теги [PERSON], [COMPANY], [AMOUNT]. Не пиши никаких приветствий и объяснений, верни ТОЛЬКО зашифрованный текст.
    
Текст для обработки: "Сегодня Maria Rossi подписала конфиденциальный контракт с корпорацией Dell на сумму 45000 евро." """,
    "stream": False
}

# Кодируем данные в JSON
req_data = json.dumps(data).encode("utf-8")

# Создаем запрос
req = urllib.request.Request(url, data=req_data, headers={'Content-Type': 'application/json'})

# Отправляем запрос и ждем ответ от ноутбука
try:
    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        result = json.loads(response_body)
        print("\n--- Ответ от локальной Ламы ---")
        print(result.get("response", "Нет ответа"))
        print("-------------------------------\n")
except Exception as e:
    print(f"Ошибка соединения с Ollama: {e}")