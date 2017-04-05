from socket import *

CONST_ADD_NEW_SERVERS_PORT = 9090

#socket will listen to port specified by user
serverPort = int(input("Type port to listen: "))

#creates client socket. It will request to servermanager to add
#a new server to the list
with open("server_ip.txt") as file:
	cont = file.read()
cont = cont.strip()

#determine sockets parameters (name/ip address and port)
serverName = cont
#creates socket
clntSocket = socket(AF_INET, SOCK_STREAM) #IPv4, UDP
clntSocket.connect((serverName, CONST_ADD_NEW_SERVERS_PORT)) #port used for adding server to servermanager

#sends a message to server containing the ip address and port
#that the new server will work with
clntSocket.send(str(serverPort).encode())

receivedMessage = clntSocket.recvfrom(8)

if receivedMessage[0].decode() == "OK":
	#then create new server socket
	serverSocket = socket(AF_INET, SOCK_STREAM) #IPv4, TCP
	serverSocket.bind(('', serverPort))
	serverSocket.listen(1)
	print("The server is ready to process requests. Let servermanager know")
	#TODO: let servermanager know if server could not be created as well
	clntSocket.send("CREATED".encode())
	clntSocket.close()
	clntSocket = None

	#infinite loop (socket will always listen)
	while True:
		print("HELLO THERE")	
		#for now the server will only process one request per TCP connection
		conSocket, addr = serverSocket.accept()

		#stores data sent from client and client's adress and port, respectively
		receivedMessage = conSocket.recvfrom(2112)
		#applies changes to received message
		answerMessage = receivedMessage[0].decode().upper()
		conSocket.send(answerMessage.encode())

#else abort
print("ERROR: could not create new server. \n" +
	"ERROR CODE: " + receivedMessage[0].decode())