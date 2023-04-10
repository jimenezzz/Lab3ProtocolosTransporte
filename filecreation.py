from random import choice
from string import ascii_letters as alphabet
import sys

PATH_ARCHIVOS = "./ArchivosEnviar/"

def createfile(filename, filesize):
    with open(PATH_ARCHIVOS+filename, 'w') as f:
        for i in range(0, filesize * 1000000):
            f.write(choice(alphabet))

if __name__ == '__main__':
    #get argument 1, if it doesnt exist then use default
    filename = sys.argv[1] if len(sys.argv) > 1 else 'archivo1.txt'
    filesize = sys.argv[2] if len(sys.argv) > 2 else 1
    createfile(filename, int(filesize))