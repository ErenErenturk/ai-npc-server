import socket
from llm_interface import get_greeting, get_named_reply, get_reply_with_memory
from memory import conversation_memory, load_memory, save_memory
from player_state import load_state, update_state, get_state

HOST = "127.0.0.1"
PORT = 65432

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        load_memory()
        print("📂 Memory loaded.")
        load_state()
        print("📂 Player state loaded.")
        s.bind((HOST, PORT))
        s.listen()
        print(f"🟢 LLM NPC Server is running at {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode().strip()
                print(f"📨 Received from Unity: {data}")

                if data == "greet":
                    reply = get_greeting()
                    save_memory()  # 💾 her cevap sonrası kaydet
                elif data.startswith("name:"):
                    player_name = data.split("name:", 1)[1].strip()
                    reply = get_named_reply(player_name)
                    save_memory()  # 💾 her cevap sonrası kaydet
                elif data.startswith("introduce:"):
                    try:
                        player_id, player_name = data.split("introduce:", 1)[1].split("|", 1)
                        conversation_memory[player_id] = [
                            {"role": "system", "content": f"The player's name is {player_name}."}
                        ]
                        reply = f"✅ Name '{player_name}' introduced and stored in memory."
                        save_memory()  # 💾 her cevap sonrası kaydet
                    except Exception as e:
                        reply = f"❌ Introduce format error: {str(e)}"
                elif data.startswith("msg:"):
                    try:
                        player_id, user_message = data.split("msg:", 1)[1].split("|", 1)
                        reply = get_reply_with_memory(player_id.strip(), user_message.strip(), conversation_memory)
                        save_memory()  # 💾 her cevap sonrası kaydet
                    except Exception as e:
                        reply = f"Memory format error: {str(e)}"
                elif data.startswith("setstate:"):
                    try:
                        player_id, kv = data.split("setstate:", 1)[1].split("|", 1)
                        key, value = kv.split("=", 1)
                        update_state(player_id.strip(), key.strip(), value.strip())
                        reply = f"✅ State updated: {key.strip()} = {value.strip()}"
                    except Exception as e:
                        reply = f"❌ SetState error: {str(e)}"
                elif data.startswith("getstate:"):
                    try:
                        player_id, key = data.split("getstate:", 1)[1].split("|", 1)
                        value = get_state(player_id.strip(), key.strip())
                        if value is not None:
                            reply = f"📍 {player_id}.{key} = {value}"
                        else:
                            reply = f"⚠️ No value found for '{key}' in player '{player_id}'."
                    except Exception as e:
                        reply = f"❌ GetState error: {str(e)}"

                else:
                    reply = "I do not understand that command."

                conn.sendall(reply.encode())
                print(f"🧠 Replied: {reply}")

if __name__ == "__main__":
    run_server()


