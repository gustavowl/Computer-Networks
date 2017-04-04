from socket import *
import _thread

#this function will be responsible for keep listening to the
#input comming from the client
def persistent_socket_connection(con_socket):
	#reads message sent from client
	receivedMessage = conSocket.recvfrom(2112)

	#if receivedMessage[0] == "" then connection was closed
	while receivedMessage[0].decode() != "":
		print(receivedMessage[0].decode()) #debugging reasons
		#computes desired algorithm for client
		answerMessage = receivedMessage[0].decode().upper()
		#send it back to client
		con_socket.send(answerMessage.encode())
		#waits for new request or end of connection
		receivedMessage = con_socket.recvfrom(2112)
	#reference to 1994's World's cup final
	#it means "It is over"
	print("-------------CABOU!!!")

#---------------------------------------------------------------

serverPort = 9001 #socket will listen to port 12112
serverSocket = socket(AF_INET, SOCK_STREAM) #IPv4, UDP

#configures the serverSocket to keep listening to port 12112
serverSocket.bind(('', serverPort))
serverSocket.listen(2)
print("The server is ready to receive")

#infinite loop (this threads' socket will always listen for new connections)
while True:
	#starts TCP connection required by client
	conSocket, addr = serverSocket.accept()

	#creates thread that will run the connection socket behavior while
	#the current thread will be responsible for listening to new connections.
	#The new thread will start running at persistent_socket_connection
	#function that receives a socket as parameter
	_thread.start_new_thread(persistent_socket_connection, (conSocket, ))