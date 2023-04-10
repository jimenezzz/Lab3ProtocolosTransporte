import socket
from _thread import *
import threading
from datetime import datetime
import hashlib
import os
import sys

PATH_ARCHIVOS = "./ArchivosEnviar/"
PATH_LOGS = "./LogsServidor/"
CHUNK_SIZE = 65536
HOST = ''
PORT = 2002

#ARCHIVO_MANDAR = 'archivo1.txt'
print_lock = threading.Lock()

def write_log(time1, arch):
    time2 = datetime.now()
    time_diff = time2 - time1
    tsecs = time_diff.total_seconds()
    format = time2.strftime('%Y-%m-%d-%H-%M-%S')

    f = open(PATH_LOGS+format+"-log.txt", "a")
    f.write(arch+", "+str(os.path.getsize(PATH_ARCHIVOS+arch))+" bytes, "+str(tsecs)+" segundos\n")
    f.close()

# Threaded function
def threaded(client, addr, archivo):
    print(f'Conexión establecida a {addr}.')
    time1 = datetime.now()

    #Se envia nombre del archivo y tamaño
    client.send((archivo+"-"+str(os.path.getsize(PATH_ARCHIVOS+archivo))).encode())

    #Se calcula el Hash del archivo
    hashmd5 = hashlib.md5() 
    with open(PATH_ARCHIVOS+archivo, 'rb') as f:
        for bloque in iter(lambda: f.read(4096), b""):
                hashmd5.update(bloque)
    client.send(hashmd5.hexdigest().encode())    
    print(hashmd5.hexdigest())        

    # Abrir el archivo para lectura
    with open(PATH_ARCHIVOS+archivo, 'rb') as f:
        while True:
            # Leer un chunk del archivo
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                # Si no quedan más datos, salir del bucle
                print_lock.release()
                break
            # Enviar el chunk al cliente
            client.send(chunk)

    write_log(time1,archivo)

    # Connection closed
    client.close()
    print(f'Conexión cerrada a {addr}.')

def main():
   archivo=input("¿Que archivo desea enviar? (1:100MB, 2:250MB)")
   if archivo=="1":
       arch = 'archivo1.txt'
   else:
       arch = 'archivo2.txt'    
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind((HOST, PORT))
   print("Enlace al puerto", PORT)

   # Put the socket into listening mode
   server.listen(5)
   print("Esperando conexión...")

   # An infinite loop until the client exits
   while True:
       # Establish connection with client
       c, addr = server.accept()
       # Lock acquired by client
       print_lock.acquire()

       # Start the new thread and return its identifier
       start_new_thread(threaded, (c,addr,arch))
   server.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ARCHIVO_MANDAR = sys.argv[1]
    main()