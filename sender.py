# -*- coding: utf-8 -*-
"""
Master CyberSecurite & CyberCriminalite  - Ensa Tanger
Author : BATALI OUALID 
Date : 30 Octobre 2019
Python version : Python 3.6.7
______________TP : Athentification using Hash function and symmetric encryption ____________
				
"""

import socket
import os
import cryptography
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


HOST = "172.15.179.130" 
PORT = 12345 # 

connexion_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_socket.connect((HOST, PORT))
print("\n[*] Connected to " +HOST+ " on port " +str(PORT)+ ".\n")


################### GENERATION DE LA CLE ####################################
private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048,
                backend=default_backend()) # Private key
public_key = private_key.public_key() # Public key

pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)
deviceID = str(input("Enter Your DeviceID :"))
email = str(input("Enter Your Email Address :"))
message = str(input("Enter Your Message :"))
print('THE PUBLIC KEY OF THE SENDER \n', pem)
signature = private_key.sign(message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256())

print("Signature", signature)
data = deviceID+"|*|"+email+"|*|"+message+"|*|"+pem+"|*|"+signature
################## VERIFICATION DE LA SIGNATURE ###############################

connexion_socket.send(data)

#connexion_socket.close()
	
