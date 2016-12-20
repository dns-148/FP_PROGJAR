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
ftp_data_socket = None
response_regex = None

def send_ftp_server(S):
	ftp_command = S + break_line
	ftp_socket.send(ftp_command)
	temp = ftp_socket.recv(max_line)
	sys.stdout.write(temp)
	return

def enter_pasv():
	ftp_command = 'PASV' + break_line
	ftp_socket.send(ftp_command)
	ftp_response = ftp_socket.recv(max_line)
	error_flag = ''

	if ftp_response[:3] != '227':
		error_flag = 'Error'

	if error_flag != 'Error':
		global response_regex
		if response_regex is None:
			import re
			response_regex = re.compile(r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)')
		result = response_regex.search(ftp_response)
		add_group = result.groups()
		port = (int(add_group[4]) * 256) + int(add_group[5])
		host = ftp_socket.getpeername()[0]
		return host, port

	else:
		sys.stdout.write(ftp_response)
		return error_flag, 0

def other(command):
	ftp_command = command + break_line
	ftp_socket.send(ftp_command)
	response = ftp_socket.recv(max_line)
	print str(response).strip()
	return

def listing_directory():
	other('TYPE A')
	ftp_data_host, ftp_data_port = enter_pasv()
	ftp_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ftp_data_socket.connect((ftp_data_host, ftp_data_port))
	ftp_command = 'LIST'+ break_line
	ftp_socket.send(ftp_command)
	ftp_data = ftp_data_socket.recv(max_line)
	sys.stdout.write(str(ftp_data))
	response = ftp_socket.recv(max_line)
	print str(response).strip()
	return

ftp_socket = socket.create_connection((ftp_host, ftp_port), def_timeout)
welcome_msg = str(ftp_socket.recv(2048)).strip()
print welcome_msg

while True:
	try:
		command = raw_input()
	    
		if 'RETR' in command:
			ftp_data_host, ftp_data_port = enter_pasv()
			ftp_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ftp_data_socket.connect((ftp_data_host, ftp_data_port))
			send_ftp_server(command)
			filename = command.split(' ')
			with open(filename[1], 'wb') as file:
				while True:
					temp = ftp_data_socket.recv(max_line)
					file.write(temp)
					flag = ftp_socket.recv(max_line)
					if '226' in flag:
						sys.stdout.write(flag)
						file.close()
						break
			ftp_data_socket.close()
		
		if 'LIST' in command:
			listing_directory()
	    
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
