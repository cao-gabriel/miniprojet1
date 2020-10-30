#!/bin/python3.8
import socket as s
import time as t
SERVERPORT = 5678
def main():
    socket_server = s.socket(s.AF_INET, s.SOCK_STREAM)
    socket_server.bind(((''), SERVERPORT))
    socket_server.listen(10)
    print("server ready")
    while True:
        connection_socket_with_proxy, adress = socket_server.accept()
        message = connection_socket_with_proxy.recv(2048)
        print("demande arrivé " + str(adress))
        modified_message = message.decode('utf-8')+"\n le message a bien été traité par le serveur : " + str(adress)
        print("envoi de la réponse")
        t.sleep(3)
        connection_socket_with_proxy.send(modified_message.encode('utf-8'))
        print("fermeture de la socket de connection")
        connection_socket_with_proxy.close()

main()
