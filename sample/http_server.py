import socket
import os
ROOT_DIR = r'C:\Users\Avi Fenesh\OneDrive\שולחן העבודה\networks\webroot'


def is_request_valid(request):
    error = ""
    valid = True
    req_to_check = request.split(' ')
    if req_to_check[0] == 'GET':
        if req_to_check[1] == r'/' or req_to_check[1] == '\\' or os.path.exists(ROOT_DIR+req_to_check[1]):
            if req_to_check[2] == 'HTTP/1.1':
                if req_to_check[3] == r'\r\n':
                    valid = False
                    error = None
                else: error = r"no \r\n at the end of the message"
            else: error = "not mentioned portocol version"
        else: error = 'root or file not exist'
    else: error = 'there no \'get\' request'
    return valid,error


def handle_client_request(request):


