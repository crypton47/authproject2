# -*- coding: utf-8 -*-
"""
Master CyberSecurite & CyberCriminalite  - Ensa Tanger
Author : BATALI OUALID 
Date : 31 Octobre 2019
Python version : Python 3.6.7
______________TP : Athentification using Hash function and symmetric encryption ____________
				
"""

import socket
import os
import sqlite3
import cryptography
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def insert(deviceID,email,message, publickey):
    try:
        sqliteConnection = sqlite3.connect('devices.db')
        sqlite_insert_query = """INSERT INTO `clients`
                          ('deviceid','email', 'message', 'publickey')  VALUES  (?,?,?,?)"""
        data_tuple = (deviceID, email, message , publickey)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        print("Data inserted!")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")


HOST = '0.0.0.0'  # server will bind to any IP
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creates server TCP socket  # prevents from getting timeout iss
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # 5 connections max in queue
print("\n[*] Listening on port " +str(PORT)+ ", waiting for connexions.")

# see socket documentation to understand how socket.accept works
client_socket, (client_ip, client_port) = server_socket.accept()

print("[*] Device  " +client_ip+ " connected.\n")


data = client_socket.recv(1024)
data = data.split('|*|')
deviceID = data[0]
email = data[1]
message = data[2]
pem_public = data[3]
signature = data[4]
# public_key = load_pem_public_key(pem_public, backend=default_backend())

#home/crypton/Desktop/dir/

file = open("publickey.txt","a")
file.write(pem_public)
file.close()



with open("publickey.txt", "r") as key_file:
    public_key = serialization.load_pem_public_key(
    key_file.read(),
    backend=default_backend())
print ('IOT Device ID : ', data[0])
print ('EMAIL ADDRESS : ', data[1])
print ('Message RECEIVED: ', data[2])
print ('Signature: ', data[4])
print ('Public Key of the the client device', data[3])

################## VERIFICATION DE LA SIGNATURE ###############################

try:
    public_key.verify(signature,message,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
    print ("############ L'AUTHENTIFICATION EST VERIFIEE  #########")
except:
    print ("############ ECHEC DE L'AUTHENTIFICATION      #########")
try:
    sqliteConnection = sqlite3.connect('devices.db')
    sqlite_create_table_query = '''CREATE TABLE clients (
                                deviceid TEXT PRIMARY KEY,
                                email TEXT NOT NULL UNIQUE,
                                message TEXT NOT NULL,
                                publickey text NOT NULL);'''
    cursor = sqliteConnection.cursor()
    #print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    #print("SQLite table created")
    sqliteConnection.commit()
    cursor.close()

except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        #print("sqlite connection is closed")
######################## INSERTION DES DONNES DANS LA BD ######################
print("[*]  INSERTION DES DONNES DANS LA BASE DE DONNE devices.db")
insert(deviceID,email,message, pem_public)
print("[*]   GENERATION D-UNE CLE DE SESSION PAR LE GNPA #####")
os.system('python3 gnpa.py')
# print ("La clé secrète est : {}".format(genkey()))
#server_socket.close()

