import socket
import sys
from _thread import *
from threading import Thread
from datetime import datetime
import os

PATH_ARCHIVOS_RECIBIDOS = "./ArchivosRecibidos/"
PATH_LOGS = "./LogsCliente/"
ARCHIVO_RECIBIR = 'archivo_recibido.txt'
CHUNK_SIZE = 9216
HOST = '172.16.35.133'
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
def threaded(num_cliente, cantidad_conexiones):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.settimeout(5)

    # Connect to server on local computer
    print("Conectando cliente "+str(num_cliente)+" al servidor...")
    server.sendto(b'Conectar',(HOST, PORT))
    print("Recibiendo archivo...")
    data, client_address = server.recvfrom(CHUNK_SIZE)
    filename, filesize = data.decode().split("-")
    time1 = datetime.now()
    nombreArchivo = PATH_ARCHIVOS_RECIBIDOS+"Cliente"+str(num_cliente)+"-Prueba-"+str(cantidad_conexiones)+".txt"
    with open(nombreArchivo, 'wb') as f:
        while True:
            # Leer un chunk del servidor
            try:
                data, client_address = server.recvfrom(CHUNK_SIZE)
                if not data:
                    # Si no quedan más datos, salir del bucle
                    break
                elif data == b'EOF':
                    break
                # Escribir el chunk en el archivo
                f.write(data)
            except socket.timeout:
                print('Server timed out')
                break

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