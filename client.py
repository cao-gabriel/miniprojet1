#!/bin/python3.8
import socket as s
import random as r
import time as t
PROXYIP = "127.0.0.1"
PROXYPORT = 1234

def main():
    i=0
    while(i<50):
        t.sleep(0.5)
        y = r.randint(0,9)
        socket_client = s.socket(s.AF_INET, s.SOCK_STREAM)
        socket_client.connect((PROXYIP, PROXYPORT))
        message = str(y)
        
        print("Envoi au proxy / message numero "+str(i))
        print("Requete numero "+str(y))
        
        socket_client.send(message.encode('utf-8'))

        proxy_response = socket_client.recv(2048)
        print("Réception de la réponse du proxy : ")
        socket_client.close()
        print("Reponse :\n"+proxy_response.decode('utf-8'))
        i+=1

main()
