# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:40:27 2020

@author: etudiant
"""


import socket as s
import threading as t

SERVERIP = '127.0.0.1'
SERVERPORT = 5678

PROXYPORT = 1234




def recherche(message):
    with open("listenoire.txt", 'r') as filin:
        lignes = filin.readlines()
        #print(lignes)
        for ligne in lignes:
            x=ligne.split("#")
            if(message==x[0]):
                return x[2]        
    return None



def handle_client(connection_socket_client):
    message = connection_socket_client.recv(2048)
    connection_socket_server = s.socket(s.AF_INET, s.SOCK_STREAM)
    connection_socket_server.connect((SERVERIP, SERVERPORT))
   
   
   
    resrecherche=recherche(message.decode('utf-8'))
    print(resrecherche)
    if(resrecherche!=None):
        #ajout et envoi du message
        print("message interdit")
        
        modified_message = "Demande interdite"
        print(modified_message)
        connection_socket_client.sendall(modified_message.encode('utf-8'))
        
    else: 
        connection_socket_server.sendall(message)
        print("envoi du message au serveur")
        server_response = connection_socket_server.recv(2048)
        print("reception du message venant du serveur")
        modified_message = "proxy 1234 : " + server_response.decode('utf-8')
        print("envoi du message au client")
        connection_socket_client.sendall(modified_message.encode('utf-8'))
        print("fermeture des socket")
        connection_socket_server.close()
    
    connection_socket_client.close()
    

def main():
    socket_proxy = s.socket(s.AF_INET, s.SOCK_STREAM)
    socket_proxy.bind(((''), PROXYPORT))
    socket_proxy.listen(10)
    print("proxy ready")
    while True:
        connection_socket_client, _ = socket_proxy.accept()
        
        t.Thread(target=handle_client(connection_socket_client,)).start()
main()