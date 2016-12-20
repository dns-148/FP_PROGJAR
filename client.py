import socket
import sys
from socket import _GLOBAL_DEFAULT_TIMEOUT

ftp_port = 21
def_timeout = _GLOBAL_DEFAULT_TIMEOUT
break_line = '\r\n'
max_line = 1024
ftp_reply = ''
ftp_host = '192.168.100.18'
ftp_socket = None

def send_ftp_server(S):
	ftp_command = S + break_line
	ftp_socket.send(ftp_command)
	temp = ftp_socket.recv(max_line)
	sys.stdout.write(temp)
	return

def other(command):
	ftp_command = command + break_line
	ftp_socket.send(ftp_command)
	response = ftp_socket.recv(max_line)
	print str(response).strip()
	return

# def creating_data_socket():
# 	ftp_data_host, ftp_data_port = enter_pasv()
# 	ftp_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	ftp_data_socket.connect((ftp_data_host, ftp_data_port))
# 	send_ftp_server(command)

ftp_socket = socket.create_connection((ftp_host, ftp_port), def_timeout)
welcome_msg = str(ftp_socket.recv(2048)).strip()
print welcome_msg

while True:
	try:
		command = raw_input()
	    
		if 'RNFR' in command:
			other(command)
			command2 = raw_input()
			other(command2)
		
		else:
			other(command)
			if 'QUIT' in command:
				ftp_socket.close()
				break

	except socket.error, exc:
		print exc
		if ftp_socket is not None:
			ftp_socket.close()
		sys.exit(0)
