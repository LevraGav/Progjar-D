import socket
import json
import logging
import threading
import datetime
import random
from tabulate import tabulate

server_address = ('172.16.16.101', 14000)

def make_socket(destination_address='localhost',port=14000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        logging.warning(f"connecting to {server_address}")
        sock.connect(server_address)
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def deserialization(s):
    logging.warning(f"deserialization {s.strip()}")
    return json.loads(s)

def send_command(command_str):
    addressing_server = server_address[0]
    port_server = server_address[1]
    sock = make_socket(addressing_server,port_server)

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
        result = deserialization(data_received)
        logging.warning("data received from server:")
        return result
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False

def get_player_data(nomor=0):
    cmd=f"get_player_data {nomor}\r\n\r\n"
    result = send_command(cmd)
    if (result):
        pass
    else:
        print("data transfer failure")
    return result

def see_version():
    cmd=f"versi \r\n\r\n"
    result = send_command(cmd)
    return result

def get_player_data_multithread(total_request,  proportion_data):
    total_response = 0
    texec = dict()
    temp1 = datetime.datetime.now()

    for k in range(total_request):
        # bagian ini merupakan bagian yang mengistruksikan eksekusi get_player_data secara multithread
        texec[k] = threading.Thread(
            target=get_player_data, args=(random.randint(1, 20),))
        texec[k].start()

    # setelah menyelesaikan tugasnya, dikembalikan ke main thread dengan join
    for k in range(total_request):
        if (texec[k] != -1):
            total_response += 1
        texec[k].join()

    temp2 = datetime.datetime.now()
    complete = temp2 - temp1
    proportion_data.append([total_request, total_request, total_response, complete])

if __name__ == '__main__':
    h = see_version()
    if (h):
        print(h)
    total_request = [1, 5, 10, 20]
    proportion_data = []
    
    for request in total_request:
        get_player_data_multithread(request,  proportion_data)
        
    porportion_header = ["Thread Count", "Request Count", "Response Count", "Execution Time", "Average Latency"]
    print(tabulate( proportion_data, headers=porportion_header, tablefmt="fancy_grid"))
