from socket import *
import _thread

debug = True

def initialize_client_socket(ip, port):
	client_socket = socket(AF_INET, SOCK_STREAM) #IPv4, TCP
	client_socket.connect((ip, port))
	#TODO: return none case fails to initialize or
	#cannot connect to server
	return client_socket

def debug(text):
	if debug:
		print(text)

#this function will be responsible for keep listening to the
#input comming from the client
def persistent_socket_connection(con_socket):
	#reads message sent from client
	receivedMessage = conSocket.recvfrom(2112)

	#if receivedMessage[0] == "" then connection was closed
	while receivedMessage[0].decode() != "":
		debug(receivedMessage[0].decode())

		#creates client socket to connect with desired server
		#TODO: info about IP and port may be stored somewhere
		#else, i.e. not static
		client_socket = initialize_client_socket('192.168.0.31', 9009)
		#TODO: treat exception: client_socket = None
		message = "servermanager says hello"
		client_socket.send(message.encode()) #server will process request
		answerMessage = client_socket.recvfrom(2112) #waits for server answer
		answerMessage = answerMessage[0].decode();
		debug("Message received from server: " +  answerMessage)

		#close connection between servermanager and server
		#TODO: ? free server to be used by other sockets ?
		client_socket.close()

		#send processed request back to client
		con_socket.send(answerMessage.encode())
		#waits for new request or end of connection
		receivedMessage = con_socket.recvfrom(2112)
	#reference to 1994's World's cup final
	#it means "It is over"
	debug("-------------CABOU!!!")

#---------------------------------------------------------------

class StructServer():
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port

#contains the list of servers that are added dynamically.
#For now, the list only increases. It is not possible
#to remove a running server, even though connection errors
#may happen
serverlist = []

def add_new_server_socket_loop():
	serverPort = 9090
	serverSocket = socket(AF_INET, SOCK_STREAM) #IPv4, UDP	
	serverSocket.bind(('', serverPort))
	serverSocket.listen(1)
	print("Server Manager is ready to add new servers dynamically")
	while True:
		conSocket, addr = serverSocket.accept()
		message = conSocket.recvfrom(8)
		serverPort = int(message[0].decode())
		#TODO: verify if it is OK to add new server, e.g. if the max
		#number of supported servers has been reached, return FAIL
		conSocket.send("OK".encode()) #says it is OK to add new server
		
		#waits for info confirming if the new server is already running
		message = conSocket.recvfrom(8)
		#TODO: add server to list instead of just printing info
		serverlist.append(StructServer(addr[0], serverPort))

		for i in range(len(serverlist)):
			print(serverlist[i].ip + '\t' + str(serverlist[i].port))

_thread.start_new_thread(add_new_server_socket_loop, ())

#servermanager needs at least one server to manage (obvious)
print("Waiting for first server connection")
length = len(serverlist)
while length == 0:
	length = len(serverlist)

serverPort = 9000 #socket will listen to port 12112
serverSocket = socket(AF_INET, SOCK_STREAM) #IPv4, UDP
#configures the serverSocket to keep listening to port 12112
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
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