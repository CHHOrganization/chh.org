import datetime
from concurrent.futures import thread
import threading
import socket
now = datetime.datetime.now()
#Colors Codes With Their Given Names
#Bright Text Colors
Dark_Black = "\u001b[30;1m"
Dark_Red = "\u001b[31;1m"
Dark_Green = "\u001b[32;1m"
Dark_Yellow = "\u001b[33;1m"
Dark_Blue = "\u001b[34;1m"
Dark_Magenta = "\u001b[35;1m"
Dark_Cyan = "\u001b[36;1m"
Dark_White = "\u001b[37;1m"

#Dark Text Colors 
Bright_Black = "\u001b[30m"
Bright_Red = "\u001b[31m"
Bright_Green = "\u001b[32m"
Bright_Yellow = "\u001b[33m"
Bright_Blue = "\u001b[34m"
Bright_Magenta = "\u001b[35m"
Bright_Cyan = "\u001b[36m"
Bright_White = "\u001b[37m"

#Bright Background Colors 
BG_Dark_Black = "\u001b[40;1m"
BG_Dark_Red = "\u001b[41;1m"
BG_Dark_Green = "\u001b[42;1m"
BG_Dark_Yellow = "\u001b[43;1m"
BG_Dark_Blue = "\u001b[44;1m"
BG_Dark_Magenta = "\u001b[45;1m"
BG_Dark_Cyan = "\u001b[46;1m"
BG_Dark_White = "\u001b[47;1m"

#Dark Background Colors 
BG_Bright_Black = "\u001b[40m"
BG_Bright_Red = "\u001b[41m"
BG_Bright_Green ="\u001b[42m"
BG_Bright_Yellow = "\u001b[43m"
BG_Bright_Blue = "\u001b[44m"
BG_Bright_Magenta = "\u001b[45m"
BG_Bright_Cyan = "\u001b[46m"
BG_Bright_White = "\u001b[47m"

#Rest Color
Rest = "\u001b[0m"

Host = '127.3.4.68'
Port = 7437

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind((Host, Port))
Server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('EXIT'):
                name_to_exit = msg.decode('ascii')[5:]
                exit_user(name_to_exit)
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{Bright_Red + nickname + Bright_Yellow} Left the Pool!'.encode('ascii'))
            nicknames.remove(nickname)
            Logout_time = datetime.datetime.now()
            print(f'{Bright_Red + nickname + Bright_Green} Left the Pool, at {Bright_Yellow + Logout_time.strftime("%H:%M:%Ss ")}')
            break
def receive():
    while True:
        
        client, address = Server.accept()
        Login_Time = datetime.datetime.now()
        print(f"{Bright_Green}connected with {Bright_Red + str(address) + Bright_Green } At; " + Bright_Yellow + Login_Time.strftime("%H:%M:%Ss "))
        

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(Bright_Green + f'Nickname of the client is {Bright_Red + nickname + Bright_Green}!')
        broadcast(f'{Bright_Red + nickname + Bright_Green} Dived into the Pool!'.encode('ascii'))
        client.send(f'{Bright_Green} Welcome To The Pool!\n\
'.encode('ascii'))
        client.send(f'{Bright_Green} You are now connected to CHH Org Network'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        print(f"{Bright_Red + BG_Bright_Green} [ACTIVE CONNECTIONS] {threading.active_count() - 1} User/s {Rest}")

def exit_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_exit = clients[name_index]
        clients.remove(client_to_exit)
        client_to_exit.send('You just left the Pool!'.encode('ascii'))
        client_to_exit.close()
        nicknames.remove(name)
        broadcast(f'{name} Left the Pool!'.encode('ascii')) 

print(Bright_Red + "Server is listening...")
receive()
