from socket import *
import _thread

CONST_MANAGE_REQUEST_PORT = 12114
CONST_ADD_NEW_SERVERS_PORT = 9090
CONST_BUFFER_SIZE = 200000

debug = True

def initialize_client_socket(ip, port):
	client_socket = socket(AF_INET, SOCK_STREAM) #IPv4, TCP
	client_socket.connect((ip, port))
	#TODO: return none case fails to initialize or
	#cannot connect to server
	return client_socket

def debug(text):
	if debug:
		print("#DEBUG: " + text)

#this function will be responsible for keep listening to the
#input comming from the client
#con_socket receives the connection stablished with the client
#server_address is a tuple containing the IP address and the port
#with which the server is working, respectively
def persistent_socket_connection(con_socket, server_address):
	#reads message sent from client
	receivedMessage = conSocket.recvfrom(CONST_BUFFER_SIZE)
	receivedMessage = receivedMessage[0].decode()

	#if receivedMessage[0] == "" then connection was closed
	while receivedMessage != "":
		debug("YTYKHH" + str(len(receivedMessage)))

		#creates client socket to connect with desired server
		client_socket = initialize_client_socket(server_address[0], server_address[1])

		#TODO: treat exception: client_socket = None
		client_socket.send(receivedMessage.encode()) #server will process request
		answerMessage = client_socket.recvfrom(CONST_BUFFER_SIZE) #waits for server answer
		answerMessage = answerMessage[0].decode();
		#debug("Message received from server: " +  answerMessage)

		#close connection between servermanager and server
		#TODO: ? free server to be used by other sockets ?
		client_socket.close()

		#send processed request back to client
		con_socket.send(answerMessage.encode())
		#waits for new request or end of connection
		receivedMessage = con_socket.recvfrom(CONST_BUFFER_SIZE)
		receivedMessage = receivedMessage[0].decode()
	#reference to 1994's World's cup final
	#it means "It is over"
	debug("-------------CABOU!!!")

#---------------------------------------------------------------

#Contains the list of servers that are added dynamically.
#It is a list of tuples, where the first element, i.e. [0],
#is the IP address (str) and the second element, i.e. [1].
#is the port (int)
#For now, the list only increases. It is not possible
#to remove a running server, even though connection errors
#may happen
serverlist = []

def add_new_server_socket_loop():
	serverSocket = socket(AF_INET, SOCK_STREAM) #IPv4, UDP	
	serverSocket.bind(('', CONST_ADD_NEW_SERVERS_PORT))
	serverSocket.listen(1)
	print("Server Manager is ready to add new servers dynamically")
	while True:
		conSocket, addr = serverSocket.accept()
		message = conSocket.recvfrom(8)
		serverPort = int(message[0].decode())
		
		#verifies if a reserved port was requested
		if (serverPort == CONST_ADD_NEW_SERVERS_PORT or
			serverPort == CONST_MANAGE_REQUEST_PORT):
			conSocket.send("INV_PORT".encode())
		else:
			#verifies if socket tuple is already being used
			is_tuple_used = False
			i = 0
			while i < len(serverlist) and not is_tuple_used:
				if (serverlist[i][0] == addr[0] and serverlist[i][1] == serverPort):
					is_tuple_used = True
				i += 1

			if is_tuple_used:
				#tuple already registered
				conSocket.send("INV_TUPL".encode())
			else:
				conSocket.send("OK".encode())
				
				#waits for info confirming if the new server is already running
				message = conSocket.recvfrom(8)
				#TODO: add server to list instead of just printing info
				serverlist.append((addr[0], serverPort))
				debug("list of active servers: " + str(serverlist))

_thread.start_new_thread(add_new_server_socket_loop, ())

#servermanager needs at least one server to manage (obvious)
print("Waiting for first server connection")
length = len(serverlist)
while length == 0:
	length = len(serverlist)

serverPort = CONST_MANAGE_REQUEST_PORT #socket will listen to port 12112
serverSocket = socket(AF_INET, SOCK_STREAM) #IPv4, UDP
#configures the serverSocket to keep listening to port 12112
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

next_server = 0 #used for computing round robin
#infinite loop (this threads' socket will always listen for new connections)
while True:
	#starts TCP connection required by client
	conSocket, addr = serverSocket.accept()

	#computes which server will proccess the new request (round robin)
	next_server = (next_server + 1) % len(serverlist)

	#creates thread that will run the connection socket behavior while
	#the current thread will be responsible for listening to new connections.
	#The new thread will start running at persistent_socket_connection
	#function that receives a socket as parameter
	_thread.start_new_thread(persistent_socket_connection, (conSocket, 
		serverlist[next_server],))