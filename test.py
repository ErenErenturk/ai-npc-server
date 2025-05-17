import socket

def send_to_server(message: str):
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode())
        response = s.recv(4096).decode()
        return response

if __name__ == "__main__":
    print("🔹 TEST MENU 🔹")
    print("1. greet")
    print("2. name:<your_name>")
    print("3. memory: msg:<name>|<message>")
    print("4. introduce:<id>|<name>")
    print("5. custom message")
    print("6. set state:<id>|<key>=<value>")
    print("7. get state:<id>|<key>")
    
    choice = input("Select test (1-6): ").strip()

    if choice == "1":
        msg = "greet"
    elif choice == "2":
        name = input("Enter player name: ").strip()
        msg = f"name:{name}"
    elif choice == "3":
        name = input("Enter player id: ").strip()
        text = input("Message to NPC: ").strip()
        msg = f"msg:{name}|{text}"
    elif choice == "4":
        player_id = input("Player ID: ").strip()
        player_name = input("Player Name: ").strip()
        msg = f"introduce:{player_id}|{player_name}"
    elif choice == "5":
        msg = input("Enter raw message: ").strip()
    elif choice == "6":
        player_id = input("Player ID: ").strip()
        key = input("Key: ").strip()
        value = input("Value: ").strip()
        msg = f"setstate:{player_id}|{key}={value}"
    elif choice == "7":
        player_id = input("Player ID: ").strip()
        key = input("Key: ").strip()
        msg = f"getstate:{player_id}|{key}"

    else:
        print("Invalid choice.")
        exit()

    print(f"\n📤 Sending: {msg}")
    print("🧠 Response:\n" + send_to_server(msg))
