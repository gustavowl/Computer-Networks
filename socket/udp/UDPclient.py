from socket import *

#this will read the server's IP address from a file
#the file is not uploaded to github. Just create a file
#with the same name and put the required IP address there
#with all the dots. e.g. 127.0.0.1
with open("server_ip.txt") as file:
	cont = file.read()
cont = cont.strip()

#determine sockets parameters (name/ip address and port)
serverName = cont
serverPort = 12112
#creates socket
clntSocket = socket(AF_INET, SOCK_DGRAM) #IPv4, UDP

#reads message to be processed by server
message = input('Input lowercase sentence:')

#application calls the socket and it will send data to the server
#encode converts message to bytes type
clntSocket.sendto(message.encode(), (serverName, serverPort))



#now client application waits for server answer
#it will return the processed message, the server info (which is already known)
#and the message will me stored at a buffer with size 2112
receivedMessage, serverAddressAndPort = clntSocket.recvfrom(2112)
#receivedMessage will be received in bytes format. convert to string before printing
print(receivedMessage.decode())
clntSocket.close()