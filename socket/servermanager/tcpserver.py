from socket import *
import _thread

def first_thread():
	for i in range(100):
		print("THREAD 1")

def second_thread():
	for i in range(100):
		print("\tTHREAD 2")

serverPort = 9001 #socket will listen to port 12112
serverSocket = socket(AF_INET, SOCK_STREAM) #IPv4, UDP

#configures the serverSocket to keep listening to port 12112
serverSocket.bind(('', serverPort))
serverSocket.listen(2)
print("The server is ready to receive")

_thread.start_new_thread( first_thread, () )
_thread.start_new_thread( second_thread, () )

#infinite loop (socket will always listen)
while True:
	conSocket, addr = serverSocket.accept()
	#stores data sent from client and client's adress and port, respectively
	connection_closed = False
	receivedMessage = conSocket.recvfrom(2112)
	while receivedMessage[0].decode() != "":
		print(receivedMessage[0].decode())
		#applies changes to received message
		answerMessage = receivedMessage[0].decode().upper()
		conSocket.send(answerMessage.encode())
		receivedMessage = conSocket.recvfrom(2112)
	print("stop it please")