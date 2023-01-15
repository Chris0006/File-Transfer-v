import socket,threading,random
HOST='127.0.0.1'  # server IP address
PORT=4444              # server port
DOWNLOAD_PORT=4443     # port for downloading
BUFFER=1024*128*1000*10
FORMAT='ascii'

alias=""
randchars="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
for char in range(30):alias+=random.choice(randchars)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            print(message)
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
        message = input(f'{alias} > ')
        client.send(message.encode(FORMAT))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
