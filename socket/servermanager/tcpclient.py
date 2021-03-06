from socket import *

CONST_MANAGE_REQUEST_PORT = 12115
CONST_BUFFER_SIZE = 200000

#this will read the server's IP address from a file
#the file is not uploaded to github. Just create a file
#with the same name and put the required IP address there
#with all the dots. e.g. 127.0.0.1
with open("server_ip.txt") as file:
	cont = file.read()
cont = cont.strip()

#determine sockets parameters (name/ip address and port)
serverName = cont
serverPort = CONST_MANAGE_REQUEST_PORT
#creates socket
clntSocket = socket(AF_INET, SOCK_STREAM) #IPv4, UDP
clntSocket.connect((serverName, serverPort))

#reads array to be sorted
with open("array.txt") as f:
	content = f.read()
#print(str(content).encode().decode()) #prints array
#prints necessary buffer size for this array
print("IRL " + str(len(content.encode())))

#first sends size of package being sent
clntSocket.send(str(len(content.encode())).encode())

#waits for message of server saying it is ready to receive
receivedMessage = clntSocket.recvfrom(8)
if (receivedMessage[0].decode() == "OK"):

	#application calls the socket and it will send data to the server
	#encode converts message to bytes type
	clntSocket.send(content.encode())

	#receivedMessage will be received in bytes format. convert to string before printing
	receivedMessage = ""
	#message may be splitted in many packages. This loops waits until all packages
	#from the server are received
	while len(receivedMessage.encode()) < len(content.encode()):
		receivedMessage += (clntSocket.recvfrom(CONST_BUFFER_SIZE))[0].decode()

	print("IRL2 " + str(len(receivedMessage)))
	#receivedMessage = receivedMessage[0].decode()
	#close connection
	clntSocket.close()
	#print(receivedMessage)

	#saves return to file
	file = open("result.txt", "w")
	file.write(receivedMessage)
	file.close()

	#verifies if list is sorted
	lst = [int(num) for num in receivedMessage.split()]
	sorted = True
	index = 1
	#print("List length: {}".format(len(lst)))
	while (sorted and index < len(lst)):
		if lst[index] < lst[index - 1]:
			sorted = False
			print("list is not sorted")
		index += 1

	if sorted:
		print("list is sorted")

else:
	print("Transaction not accepted by server")