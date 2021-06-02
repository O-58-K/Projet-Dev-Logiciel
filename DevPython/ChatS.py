import socket 
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip, port = "127.0.0.1", 50 # Adresse Ip locale ou celle d'un serveur réel
server.bind((ip, port))
server.listen(4)
clientC = True # Condition de démarrage
clientR = [server]

print("Vous pouvez discuter entre joueurs pendant ou après la partie")

while clientC: # Condition en cours

	liste_lu, liste_acce_Ecrit, exception = select.select(clientR, [], clientR)

	for clientRo in liste_lu:

		if clientRo is server:
			client, AdresseIP = server.accept()
			print(f"Connexion en cours de : {client} - AdresseIP: {AdresseIP}")
			clientR.append(client)

		else:
			donnees_recus = clientRo.recv(128).decode("utf-8")
			if donnees_recus:
				print(donnees_recus)

			else:
				clientR.remove(clientRo)
				print("quelqu'un est parti")
				print(f"Il ne reste plus que {len(clientR) - 1} personne(s)")


