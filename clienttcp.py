import socket
import sys
from _thread import *
from threading import Thread
from datetime import datetime
import os
import hashlib

PATH_ARCHIVOS_RECIBIDOS = "./ArchivosRecibidos/"
PATH_LOGS = "./LogsCliente/"
ARCHIVO_RECIBIR = 'archivo_recibido.txt'
CHUNK_SIZE = 65536
HOST = '192.168.187.128'
PORT = 2002

NUM_CLIENTES = 1

def write_log(time1, filename, filesize, received_file):
    time2 = datetime.now()
    time_diff = time2 - time1
    tsecs = time_diff.total_seconds()
    format = time2.strftime('%Y-%m-%d-%H-%M-%S')

    if int(filesize) == os.path.getsize(received_file):
        confirmacion="archivo recibido correctamente"
    else:
        confirmacion="archivo recibido incompleto"

    f = open(PATH_LOGS+format+"-log.txt", "a")
    f.write(filename+", "+confirmacion+", tamaño original "+filesize+" bytes, "+str(os.path.getsize(received_file))+" bytes recibidos, "+str(tsecs)+" segundos\n")
    f.close()

# Threaded function
def threaded(num_cliente, cantidad_conexiones, ):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # Connect to server on local computer
    print("Conectando cliente "+str(num_cliente)+" al servidor...")
    server.connect((HOST, PORT))
    print("Recibiendo archivo...")
    data = server.recv(CHUNK_SIZE)
    hash=server.recv(CHUNK_SIZE).decode()
    print(hash)
    filename, filesize = data.decode().split("-")
    time1 = datetime.now()
    nombreArchivo = PATH_ARCHIVOS_RECIBIDOS+"Cliente"+str(num_cliente)+"-Prueba-"+str(cantidad_conexiones)+".txt"
    with open(nombreArchivo, 'wb') as f:
        while True:
            # Leer un chunk del servidor
            data = server.recv(CHUNK_SIZE)
            if not data:
                # Si no quedan más datos, salir del bucle
                break
            # Escribir el chunk en el archivo
            f.write(data)

    write_log(time1, filename, filesize, nombreArchivo)
    # Close the connection
    print("Archivo recibido y guardado en", nombreArchivo)
    server.close()

def main():
    for i in range(0, NUM_CLIENTES):
        Thread(target = threaded, args = (i+1,NUM_CLIENTES)).start()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        NUM_CLIENTES = int(sys.argv[1])
    main()