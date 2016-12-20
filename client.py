import socket
import sys
from socket import _GLOBAL_DEFAULT_TIMEOUT

def_timeout = _GLOBAL_DEFAULT_TIMEOUT
break_line = '\r\n'
max_line = 1024
ftp_port = 3004
ftp_host = '10.181.1.240'
ftp_socket = None

def send_to_server(command):
	ftp_command = command + break_line
	ftp_socket.send(ftp_command)
	ftp_response = ftp_socket.recv(max_line)
	print str(ftp_response).strip()
	return

def download(command):
	ftp_socket.send(command + break_line)
	filename = command.split(' ')
	with open(filename[1], 'wb') as file:
		while True:
			temp = ftp_socket.recv(max_line)
			if '226' in temp:
				print temp.strip()
				file.close()
				break
			else:
				file.write(temp)

def upload(command):
	ftp_socket.send(command + break_line)
	filename = command.split(' ')
	content = open(filename[1], 'r').read()
	ftp_socket.sendall(content + break_line)
	ftp_response = ftp_socket.recv(max_line).strip()
	print ftp_response

ftp_socket = socket.create_connection((ftp_host, ftp_port), def_timeout)
welcome_msg = ftp_socket.recv(2048).strip()
print welcome_msg

while True:
	try:
		command = raw_input()
	    
		if 'RETR' in command:
			download(command)
		elif 'STOR' in command:
			upload(command)
		elif 'RNFR' in command:
			send_to_server(command)
			command2 = raw_input()
			send_to_server(command2)
		else:
			send_to_server(command)
			if 'QUIT' in command:
				ftp_socket.close()
				break

	except socket.error, exc:
		print exc
		if ftp_socket is not None:
			ftp_socket.close()
		sys.exit(0)
