# Avi Fenesh
# A simple http server for study and practice
# 10.10.2020

import socket
import os

PORT = 80
ROOT_DIR = r'C:\Users\Avi Fenesh\OneDrive\שולחן העבודה\networks\webroot\webroot'  # the root directory with all the info
forbidden_file = [r"C:\Users\Avi Fenesh\OneDrive\שולחן העבודה\networks\webroot\webroot\css\doremon.css",
                   r"C:\Users\Avi Fenesh\OneDrive\שולחן העבודה\networks\webroot\webroot\js\box.js"]


def is_request_valid(request, client_socket):  # check if the message received from the client are working with our protocol
    error = ""
    valid = True
    req_to_check = request.split(' ')
    if req_to_check[0] == 'GET':  # request must start with get
        if req_to_check[1] == r'/' or req_to_check[1] == '\\' or os.path.exists(
                ROOT_DIR + req_to_check[1]):  # request must ask for a valid path or folder / us reference for home page
            if req_to_check[2] == 'HTTP/1.1':  # must have this version
                if req_to_check[3] == r'\r\n': # request must end with those letter
                    if req_to_check[1] not in forbidden_file: # check if the request is one of the forbidden files
                        if os.path.basename(req_to_check[1]) != 'page1.html': # check if this the page that changed
                            valid = False
                            error = None
                        else:
                            error = r'this file has changed to page2.html'
                            client_socket.send('302 Temporarily Moved - try page2.html')
                    else:
                        error = r"this is a forbidden file"
                        client_socket.send("403 Forbidden".encode())
                else:
                    error = r"no \r\n at the end of the message"
                    client_socket.send("500 Internal Server Error".encode())
            else:
                error = "not mentioned protocol version"
                client_socket.send("500 Internal Server Error".encode())
        else:
            error = 'root or file not exist'
            client_socket.send("404 Not found".encode())
    else:
        error = 'there no \'get\' request'
        client_socket.send("500 Internal Server Error".encode())
    return valid, error


def handle_client_request(request):  # after sure the request valid, handle the request
    split_req = request.split(" ")
    if split_req[1] == '\\' or split_req[1] == '/':  # \ or/ are reference for "index.html"
        data_path = ROOT_DIR + r'\index.html'
    else:
        path = split_req[1].replace('/', '\\')
        data_path = ROOT_DIR + path
    return data_path


def send_data_to_client(client_socket, data_path):
    type_of_file = ''
    name = os.path.basename(data_path)
    end_of_file = name.split(".")[1]
    if end_of_file in ["txt", "html"]:
        type_of_file = " text/html; charset=utf-8"
    elif end_of_file in ["jpg", "png"]:
        type_of_file = " image/jpeg"
    elif end_of_file == "js":
        type_of_file = " text/javascript; charset=UTF-8"
    elif end_of_file == "css":
        type_of_file = " text/css"
    f = open(data_path, 'rb')
    data = f.read()
    data_len = len(data)
    client_socket.sendall(name.encode())
    client_socket.sendall(data)
    client_socket.send(("HTTP/1.1  200 ok \\r \\n" + "\n Content-length: "
                       + data_len + "\n" + "Content-Type:" + type_of_file).encode())
    client_socket.close()
    f.close()
    return 'file been send'


def main():
    # create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    server_socket.bind(('127.0.0.1' , 90))
    # become a server socket
    server_socket.listen()
    while True: # main loop of program
        client_socket, adrr = server_socket.accept()
        request = client_socket.recv(1024).decode()
        valid, error = is_request_valid(request, client_socket)
        if valid:
            data_path = handle_client_request(request)
            send_data_to_client(client_socket, data_path)
        else:
            print("we had a problem with the request" + error)
            client_socket.close()


if __name__ == '__main__':
    main()