from openai import OpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL
from prompts import GREETING_SYSTEM_PROMPT, NAME_SYSTEM_PROMPT

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL
)

def get_greeting():
    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-8b-instruct:free",
        temperature=0.3,
        max_tokens=60,
        messages=[
            {"role": "system", "content": GREETING_SYSTEM_PROMPT},
            {"role": "user", "content": "A player just appeared in the forest. Greet them."}
        ]
    )
    return response.choices[0].message.content.strip()

def get_named_reply(player_name):
    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        temperature=0.3,
        max_tokens=60,
        messages=[
            {"role": "system", "content": NAME_SYSTEM_PROMPT},
            {"role": "user", "content": f"The player's name is {player_name}. Greet them personally."}
        ]
    )
    return response.choices[0].message.content.strip()

def get_reply_with_memory(player_id, user_message, memory):
    # Geçmişi al ya da başlat
    messages = memory.get(player_id, [])
    
    # En fazla 10 mesajlık pencere (kısıtlı context için)
    limited_history = messages[-10:]  

    # Yeni kullanıcı mesajını ekle
    limited_history.append({"role": "user", "content": user_message})

    # LLM çağrısı
    response = client.chat.completions.create(
        model="meta-llama/llama-3.3-8b-instruct:free",
        temperature=0.3,
        max_tokens=100,
        messages=limited_history
    )

    # Cevabı ekle ve kaydet
    reply = response.choices[0].message.content.strip()
    limited_history.append({"role": "assistant", "content": reply})
    memory[player_id] = limited_history

    return reply
