import socket
import json
import base64
import logging
import time
import os

server_address=('0.0.0.0',7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        print(hasil)
        return hasil
    except:
        logging.warning("error during data receiving")
        return False

def remote_list():
    command_str=f"LIST\n"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}\n"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False
    
def remote_upload(filename=""):
    simpan = open(filename, 'rb')
   
    data = base64.b64encode(simpan.read())
    simpan.close()
    command_str=f"upload {filename} {data}\n"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        os.chdir("../")
        history = open("history.txt", 'a')
        localtime = time.asctime( time.localtime(time.time()))
        isi = f": file {filename} diupload \n"
        history.write(localtime)
        history.write(isi)
        history.close()
        print("Success!")
        return True
    else:
        print("Fail:(")
        return False
    
def remote_delete(filename=""):
    command_str=f"delete {filename}\n"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        os.chdir("../")
        history = open("history.txt", 'a')
        localtime = time.asctime( time.localtime(time.time()) )
        isi = f": file {filename} didelete \n"
        history.write(localtime)
        history.write(isi)
        history.close()
        print("Success!")
        return True
    else:
        print("Fail:(")
        return False

if __name__=='__main__':
    server_address=('0.0.0.0',6667)
    remote_list()
    os.chdir("./upload_file")
    # remote_upload('rfc2616.pdf')
    # remote_upload('pokijan.jpg')
    # remote_upload('donalbebek.jpg')
    remote_delete('donalbebek.jpg')
    # remote_delete('rfc2616.pdf')
    #remote_get('pokijan.jpg')