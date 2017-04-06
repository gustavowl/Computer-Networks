from socket import *

CONST_MANAGE_REQUEST_PORT = 9000
CONST_BUFFER_SIZE = 100000

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

#reads message to be processed by server
message = input('Input lowercase sentence:')

#application calls the socket and it will send data to the server
#encode converts message to bytes type
with open("array.txt") as f:
	content = f.readlines()
content = [x.strip() for x in content]

print(content)
print("IRL " + str(len(str(content).encode())))

clntSocket.send(str(content).encode())

receivedMessage = clntSocket.recvfrom(CONST_BUFFER_SIZE)
#receivedMessage will be received in bytes format. convert to string before printing
print(receivedMessage[0].decode())
message = "leeroy jenkins"
print(message)
clntSocket.send(message.encode())
print("send")
receivedMessage = clntSocket.recvfrom(CONST_BUFFER_SIZE)
#receivedMessage will be received in bytes format. convert to string before printing
print(receivedMessage[0].decode())

message = input('Input another lowercase sentence:')
clntSocket.send(message.encode())
print((clntSocket.recvfrom(CONST_BUFFER_SIZE))[0].decode())
clntSocket.close()
