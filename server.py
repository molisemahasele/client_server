import socket
import threading #threading allows running multiple pieces of code alongside each other

HEADER = 64 #first message to the server is going to be a header of length 64 that tells us the length of the message thats gonna come next
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #gets my ipv4 address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create our socket, AF_INET works with ipv4
server.bind(ADDR) #binding the address with the socket

def handle_client(conn, addr):
    print(f"[NEW_CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) #receive a message from the client
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
            

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() #addr gives us info about the port and address
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()
