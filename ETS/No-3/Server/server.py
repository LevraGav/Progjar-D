import socket
import logging
import json
import ssl
import threading
import os

alldata = dict()
alldata['1']=dict(nomor=1, nama="Courtois", team="Real Madrid", position="Goalkeeper")
alldata['2']=dict(nomor=2, nama="Carjaval", team="Real Madrid", position="Defender")
alldata['3']=dict(nomor=4, nama="Alaba", team="Real Madrid", position="Defender")
alldata['4']=dict(nomor=12, nama="Marcelo", team="Real Madrid", position="Defender")
alldata['5']=dict(nomor=14, nama="Casemiro", team="Real Madrid", position="Midfielder")
alldata['6']=dict(nomor=15, nama="Valverde", team="Real Madrid", position="Midfielder")
alldata['7']=dict(nomor=22, nama="Isco", team="Real Madrid", position="Midfielder")
alldata['8']=dict(nomor=7, nama="Hazard", team="Real Madrid", position="Forward")
alldata['9']=dict(nomor=9, nama="Benzema", team="Real Madrid", position="Forward")
alldata['10']=dict(nomor=11, nama="Asensio", team="Real Madrid", position="Forward")
alldata['11']=dict(nomor=1, nama="Marc-Andre ter Stegen", team="Barcelona", position="Goalkeeper")
alldata['12']=dict(nomor=3, nama="Gerard Pique", team="Barcelona", position="Defender")
alldata['13']=dict(nomor=8, nama="Dani Alves", team="Barcelona", position="Defender")
alldata['14']=dict(nomor=21, nama="Frankie de Jong", team="Barcelona", position="Midfielder")
alldata['15']=dict(nomor=7, nama="Ousmane Dembele", team="Barcelona", position="Forward")
alldata['16']=dict(nomor=9, nama="Memphis Depay", team="Barcelona", position="Forward")
alldata['17']=dict(nomor=10, nama="Ansu Fati", team="Barcelona", position="Forward")
alldata['18']=dict(nomor=12, nama="Martin Braithwaite", team="Barcelona", position="Forward")
alldata['19']=dict(nomor=19, nama="Ferran Torres", team="19", position="Forward")
alldata['20']=dict(nomor=25, nama="Pierre Emerick Aubameyang", team="Barcelona", position="Forward")

def versi():
    return "versi 0.0.1"

def proses_request(request_string):
    #format request
    # NAMACOMMAND spasi PARAMETER
    cstring = request_string.split(" ")
    hasil = None
    try:
        command = cstring[0].strip()
        if (command == 'getdatapemain'):
            # getdata spasi parameter1
            # parameter1 harus berupa nomor pemain
            logging.warning("getdata")
            nomorpemain = cstring[1].strip()
            try:
                logging.warning(f"data {nomorpemain} ketemu")
                hasil = alldata[nomorpemain]
            except:
                hasil = None
        elif (command == 'versi'):
            hasil = versi()
    except:
        hasil = None
    return hasil

def serialisasi(a):
    #print(a)
    #serialized = str(dicttoxml.dicttoxml(a))
    serialized =  json.dumps(a)
    logging.warning("serialized data")
    logging.warning(serialized)
    return serialized

def run_server(server_address, is_secure=False):
    # ------------------------------ SECURE SOCKET INITIALIZATION ----
    if is_secure == True:
        print(os.getcwd())
        cert_location = os.getcwd() + '/certs/'
        socket_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        socket_context.load_cert_chain(
            certfile=cert_location + 'domain.crt',
            keyfile=cert_location + 'domain.key'
        )
    # ---------------------------------
    
    #--- INISIALISATION ---
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    logging.warning(f"starting up on {server_address}")
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1000)
    
    threads = dict()
    thread_index = 0

    while True:
        # Wait for a connection
        logging.warning("waiting for a connection")
        koneksi, client_address = sock.accept()
        logging.warning(f"Incoming connection from {client_address}")
        # Receive the data in small chunks and retransmit it

        try:
            if is_secure == True:
                connection = socket_context.wrap_socket(
                    koneksi, server_side=True)
            else:
                connection = koneksi

            threads[thread_index] = threading.Thread(
                target=send_data, args=(client_address, connection))
            threads[thread_index].start()
            thread_index += 1

            # Clean up the connection
        except ssl.SSLError as error_ssl:
            logging.warning(f"SSL error: {str(error_ssl)}")
            
def send_data(client_address, connection):
    selesai = False
    data_received = ""  # string
    while True:
        data = connection.recv(32)
        logging.warning(f"received {data}")
        if data:
            data_received += data.decode()
            if "\r\n\r\n" in data_received:
                selesai = True

            if (selesai == True):
                hasil = proses_request(data_received)
                logging.warning(f"hasil proses: {hasil}")

                hasil = serialisasi(hasil)
                hasil += "\r\n\r\n"
                connection.sendall(hasil.encode())
                selesai = False
                data_received = ""  # string
                break

        else:
            logging.warning(f"no more data from {client_address}")
            break

if __name__=='__main__':
    try:
        run_server(('0.0.0.0', 10000), is_secure=True)
    except KeyboardInterrupt:
        logging.warning("Control-C: Program berhenti")
        exit(0)
    finally:
        logging.warning("selesai")