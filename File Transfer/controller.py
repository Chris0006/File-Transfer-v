import socket,threading
HOST='127.0.0.1'  # server IP address
PORT=4444              # server port
BUFFER=1024*128*1000*10
FORMAT='ascii'

alias = "4!TMr*xR^U39@Zc#hL*OjQ$rvl7!Ij*4$f2#KV&7NBV*JImB" # secret key
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == "alias?":
                client.send(alias.encode(FORMAT))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        message = input(">> ")
        client.send(message.encode(FORMAT))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
