#!/bin/python3.8
import socket as s
import threading as t

SERVERIP = '127.0.0.1'
SERVERPORT = 80

PROXYPORT = 1234

def handle_request(client_request):
    # request should be : GET file_name etc...
    tmp = client_request.decode('utf-8').split(' ')
    file_name = tmp[1].split("/")
    file_name = file_name[-1]
    print("The file asked by the client is : " + file_name)
    txt = ""
    try:
        with open(file_name, 'rb') as file:
            txt = file.read()
    except FileNotFoundError:
        return (0, "", file_name)

    return (1, txt, file_name)

def caching(server_response, file_name):
    with open(file_name, "wb") as file:
        file.write(server_response)

    return 0

def handle_client(connection_socket_client):
    client_request = connection_socket_client.recv(2048)
    # message should be an http request with the method GET

    (is_found, content, file_name) = handle_request(client_request)
    if is_found == 1:
        print(file_name + " has been found in the file system of server")
        print("Sending file to the client")
        connection_socket_client.sendall(content)
        print("Closing the connection with the client")
        connection_socket_client.close()
    else:
        print("File has not been found in the file system of proxy")
        print("Start connection with the server")
        connection_socket_server = s.socket(s.AF_INET, s.SOCK_STREAM)
        connection_socket_server.connect((SERVERIP, SERVERPORT))
        print("Sending the request to the server")
        connection_socket_server.sendall(client_request)
        server_response = connection_socket_server.recv(2048)
        print("Receiving the response of the request")
        caching(server_response, file_name)
        print("Sending the response to the client")
        connection_socket_client.sendall(server_response)
        print("Closing all data related connection")
        connection_socket_client.close()
        connection_socket_server.close()

def main():
    socket_proxy = s.socket(s.AF_INET, s.SOCK_STREAM)
    socket_proxy.bind(((''), PROXYPORT))
    socket_proxy.listen(10)
    print("Cache proxy is ready !!")
    while True:
        connection_socket_client, client_adress = socket_proxy.accept()
        print("Connection with the client : " + str(client_adress))
        t.Thread(target=handle_client(connection_socket_client,)).start()

main()
