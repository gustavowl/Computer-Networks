from socket import *

serverPort = 12112 #socket will listen to port 12112
serverSocket = socket(AF_INET, SOCK_DGRAM) #IPv4, UDP

#configures the serverSocket to keep listening to port 12112
serverSocket.bind(('', serverPort))
print("The server is ready to receive")

#infinite loop (socket will always listen)
while True:
	#stores data sent from client and client's adress and port, respectively
	receivedMessage, clientAdress = serverSocket.recvfrom(2112)
	#applies changes to received message
	answerMessage = receivedMessage.upper()
	serverSocket.sendto(answerMessage, clientAdress)