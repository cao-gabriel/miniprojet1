# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 13:32:32 2020

@author: etudiant
"""

 
import socket as s
import threading as t

from datetime import datetime
import os as o

SERVERIP = '127.0.0.1'
SERVERPORT = 80

PROXYPORT = 1234


#viderleslog
def cleanlog():
     fichier = open("log.txt","w")
     fichier.close()
     
     
     
  
    
def ecrirelog(message,reponse):
   
    heure=str(datetime.now())
    fichier = open("log.txt","a")

    taille=str(o.path.getsize("log.txt"))
    droit="droit"
    
    ajoutlog=message+"#"+heure+"#"+reponse+"#"+taille+"#"+droit+"\n"
    fichier.write(ajoutlog)
    
    fichier.close()
    
    
def recherchelog(message):
    with open("log.txt", 'r') as filin:
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
    resrecherche=recherchelog(message.decode('utf-8'))
    print(resrecherche)
    if(resrecherche!=None):
        #ajout et envoi du message
        print("Pas besoin d'envoyer le message au serveur on rend la réponse des logs")
        
        modified_message = "proxy 1234 : "+resrecherche
        print(modified_message)
        connection_socket_client.sendall(modified_message.encode('utf-8'))
        
    else: 
        #on se connect au serveur et on attend sa réponse 
        connection_socket_server.sendall(message)
        print("Envoi du message au serveur")
        server_response = connection_socket_server.recv(2048)
        print("Reception du message venant du serveur")
        
        #on ajoute une nouvelle ligne au fichier suivant le format choisi        
        ecrirelog(message.decode('utf-8'),server_response.decode('utf-8'))
        
        #envoi du message au client        
        modified_message = "proxy 1234 : " + server_response.decode('utf-8')
        print("Envoi du message au client")
        connection_socket_client.sendall(modified_message.encode('utf-8'))
        connection_socket_server.close()
    
    
    
    print("Fermeture des socket")
    connection_socket_client.close()
    

def main():
    socket_proxy = s.socket(s.AF_INET, s.SOCK_STREAM)
    socket_proxy.bind(((''), PROXYPORT))
    socket_proxy.listen(10)
    fichier = open("log.txt","w")
    fichier.close()
    print("PROXY Ready")
    while True:
        connection_socket_client, _ = socket_proxy.accept()
        
        t.Thread(target=handle_client(connection_socket_client,)).start()

main()
