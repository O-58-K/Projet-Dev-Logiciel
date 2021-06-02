import socket 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip, port = "127.0.0.1", 50
client.connect((ip, port))
Client = True
name = input("Nom du joueur ? ")

while Client:
	chat = input(f"{name} > ")
	client.send(f"{name} > {chat}".encode("utf-8"))



