# Lab3ProtocolosTransporte

## Paso 1: Creación archivos
Para ejecutar el servidor y el cliente de cualquiera de los dos protocolos, TCP o UDP, primero se tienen que crear los archivos a transmitir. Para eso se corre el script filecreation.py, de la siguiente forma:

python3 filecreation.py archivo100.txt 100

En el que archivo100.txt corresponde al nombre del archivo a crear y 100 al tamaño del archivo, en este caso se creará un archivo de 100Mb de letras generadas aleatoriamente.

##Paso 2: Correr servidor
Para correr el servidor se necesita escribir la siguiente línea en la terminal, esta linea depende de si se quiere correr el servidor TCP o UDP, donde cambia el sufijo del nombre del script:

python3 serverudp.py archivo100.txt

Donde archivo100.txt corresponde al archivo que el servidor va a transmitir cuando se haga una conexión a este desde un cliente.

##Paso 3: Correr cliente
Al correr el cliente se necesita pasar el número de clientes que se quieren crear para la prueba. Así pues:

python3 clientudp.py 10

Donde 10 corresponde a la simulación de 10 clientes conectados de forma concurrente al servidor udp o tcp.

##PD: en los ejemplos se usaron los clientes y servidores udp, sin embargo basta con cambiar udp por tcp en el nombre de los archivos y los scripts de tal protocolo correrán.
