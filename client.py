from socket import socket, AF_INET, SOCK_STREAM, error

client_ftp = socket(AF_INET, SOCK_STREAM)
client_ftp.connect (('10.151.43.131', 21))

welcome_msg = str(client_ftp.recv(1024)).rstrip()
print welcome_msg

while True:
    message = raw_input()
    client_ftp.send(message+'\r\n')
    try:
        response = str(client_ftp.recv(1024)).rstrip()        
      	print response.rstrip()
	if message == 'QUIT':
	    client_ftp.close()
	    break

    except error, exc:
	client_ftp.close()
	sys.exit(0)
