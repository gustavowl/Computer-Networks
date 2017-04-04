from socket import *

#socket will listen to port specified by user
serverPort = int(input("Type port to listen: "))
serverSocket = socket(AF_INET, SOCK_STREAM) #IPv4, TCP

#configures the serverSocket to keep listening to specified port
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to process requests")

#infinite loop (socket will always listen)
while True:
	#for now the server will only process one request per TCP connection
	conSocket, addr = serverSocket.accept()
	#stores data sent from client and client's adress and port, respectively
	receivedMessage = conSocket.recvfrom(2112)
	#applies changes to received message
	answerMessage = receivedMessage[0].decode().upper()
	conSocket.send(answerMessage.encode())