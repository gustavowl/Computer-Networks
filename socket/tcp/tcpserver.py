from socket import *

serverPort = 8888 #socket will listen to port 12112
serverSocket = socket(AF_INET, SOCK_STREAM) #IPv4, UDP

#configures the serverSocket to keep listening to port 12112
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

#infinite loop (socket will always listen)
while True:
	conSocket, addr = serverSocket.accept()
	#stores data sent from client and client's adress and port, respectively
	receivedMessage = conSocket.recvfrom(2112)
	#applies changes to received message
	answerMessage = receivedMessage[0].decode().upper()
	conSocket.send(answerMessage.encode())