from socket import *

CONST_ADD_NEW_SERVERS_PORT = 9090
CONST_BUFFER_SIZE = 200000

#------------------MERGE SORT IMPLEMENTATION---------------------------------------
#Explanation of algorithm can be found at
#github.com/gustavowl/Algorithms-Cormen/blob/master/Chapter02/merge_sort_recursive.py
def merge(lst, start, end):
	start = int(start)
	end = int(end)
	cp = lst[start:end]
	middle = (start + end) // 2
	index = start
	while ( middle > start and end > middle ):
		if ((cp[0]) < (cp[middle - start] )):
			lst[index] = cp.pop(0)
			middle -= 1
		else:
			lst[index] = cp.pop(middle - start)
		index += 1
		end -= 1
	while (len(cp) > 0):
		lst[index] = cp.pop(0)
		index += 1

def merge_sort(lst, start, end):
	start = int(start)
	end = int(end)
	if end - start > 1:
		merge_sort(lst, start, (start + end) // 2)
		merge_sort(lst, (start + end) // 2, end)
		merge(lst, start, end)

#------------------------------------------------------------------------------------
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
print(receivedMessage[0].decode())

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

		#receives the size (in bytes) of list to be sent
		size = int((conSocket.recvfrom(16))[0].decode())
		conSocket.send("OK".encode())

		#stores data sent from client and client's adress and port, respectively
		receivedMessage = conSocket.recvfrom(size)
		print("received message: " + str(receivedMessage[1]) + "\t" +
			"length: " + str(len(receivedMessage[0].decode())))
		receivedMessage = receivedMessage[0].decode()
		while len(receivedMessage.encode()) < size:
			receivedMessage += (conSocket.recvfrom(size))[0].decode()
			print("\tiPrinted")
		#print(receivedMessage)
		#applies changes to received message
		array = [int(num) for num in receivedMessage.split()]
		merge_sort(array, 0, len(array))
		answer = str(array).replace(',', '')
		conSocket.send(answer[1 : len(answer) - 1].encode())

#else abort
print("ERROR: could not create new server. \n" +
	"ERROR CODE: " + receivedMessage[0].decode())