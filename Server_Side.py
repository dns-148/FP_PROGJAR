import socket
import sys
import errno

max_size = 8192
user_file = open("user_list.conf", "r").read().split('\n')
user_list = {}
logged_user = {}
break_line = '\r\n'
running_message = "FUSD FTP Server 0.5.6 beta\n"
welcome_message = "220 FUSD FTP Server 0.5.6 beta "+break_line


for line in user_file:
    length = strlen(line)
    splited = line[:length-1].split('::')
    user_list[splited[0]] = splited[1]

s_address = "127.0.0.1"
s_port = 21
server_address = (s_address, s_port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)
input_socket = [server_socket, sys.stdin]
data_socket = None
threads = []


def route_response(message):
    print message


def listening_socket():
    global server_socket
    global threads
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
                client_address = client_socket.getpeername()
                if client_address[0] in logged_user:
                    status = logged_user[client_address[0]]
                else:
                    status = 'not logged in'
                log = '{:%Y/%m/%d %H:%M:%S} '.format(datetime.datetime.now())+"- "+status+'('+client_address[0]+')> '
                print(log + 'Connected on port '+str(s_port)+', sending welcome message')
                server_socket.send(welcome_message)
            else:
                client_message = str(sock.recv(1024)).strip(break_line)
                client_address = sock.getpeername()
                if client_address[0] in logged_user:
                    status = logged_user[client_address[0]]
                else:
                    status = 'not logged in'
                log = '{:%Y/%m/%d %H:%M:%S} '.format(datetime.datetime.now()) + "- " + status
                print log + '(' + client_address[0] + ')> ' + client_message

                route_response(client_message)


try:
    t_main = threading.Thread(listening())
    t_main.start()
    threads.append(t_main)
except KeyboardInterrupt:
    for th in threads:
        th.join()
    server_socket.close()
    sys.exit(0)
