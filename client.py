import socket

def parse_packet(packet):
    parts = packet.split("|")
    if len(parts) != 3:
        return packet
    data, method, control = parts
    return f"{data}\n[Method: {method} | Control: {control}]\n"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8080))

    while True:
        try:
            msg = client.recv(1024).decode()
            print(parse_packet(msg))

            if "Enter cell number" in msg:
                move = input("Your move: ")
                client.sendall(move.encode())
        except:
            print("Disconnected")
            break

if __name__== '__main__':
    main()