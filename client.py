import socket
import sys
from socket import _GLOBAL_DEFAULT_TIMEOUT

def_timeout = _GLOBAL_DEFAULT_TIMEOUT
break_line = '\r\n'
max_line = 1024
ftp_port = 3004
ftp_host = '10.181.1.237'
ftp_socket = socket.create_connection((ftp_host, ftp_port), def_timeout)
welcome_msg = ftp_socket.recv(2048).strip()
print welcome_msg


def send_to_server(command):
    ftp_command = command + break_line
    ftp_socket.send(ftp_command)
    ftp_response = ftp_socket.recv(max_line)
    print str(ftp_response).strip()
    return


def download(command):
    ftp_socket.send(command + break_line)
    temp = ftp_socket.recv(max_line)
    filename = command.split(' ')
    if '550' in temp:
        print filename
    else:
        s_file = open(filename[1], 'wb')
        while True:
            temp = ftp_socket.recv(max_line)
            if '226' in temp:
                print temp.strip()
                s_file.close()
                break
            else:
                s_file.write(temp)


def upload(command):
    ftp_socket.send(command + break_line)
    filename = command.split(' ')
    content = open(filename[1], 'r').read()
    ftp_socket.sendall(content + break_line)
    ftp_response = ftp_socket.recv(max_line).strip()
    print ftp_response


def list_func(command):
    ftp_command = command + break_line
    ftp_socket.send(ftp_command)
    ftp_response = ftp_socket.recv(max_line)
    print(ftp_response.strip())
    ftp_response = ftp_socket.recv(max_line)
    print(ftp_response.strip())

def help_func(command):
    ftp_command = command + break_line
    ftp_socket.send(ftp_command)
    ftp_response = ftp_socket.recv(max_line)
    print(ftp_response.strip())
    ftp_response = ftp_socket.recv(max_line)
    print(ftp_response.strip())


while True:
    try:
        m_command = raw_input()

        if 'RETR' in m_command:
            download(m_command)
        elif 'STOR' in m_command:
            upload(m_command)
        elif 'RNFR' in m_command:
            send_to_server(m_command)
            command2 = raw_input()
            send_to_server(command2)
        elif 'LIST' in m_command:
            list_func(m_command)
        elif 'HELP' in m_command:
            help_func (m_command)
        else:
            send_to_server(m_command)
            if 'QUIT' in m_command:
                ftp_socket.close()
                break

    except socket.error, exc:
        print exc
        if ftp_socket is not None:
            ftp_socket.close()
        sys.exit(0)
