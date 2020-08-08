# peer.py
'''
A P2P client
It provides the following functions:
- Register the content file to the index server (R)
- Contact the index server to search for a content file (D) 
    - Contact the peer to download the file
    - Register the content file to the index server
- De-register a content file (T)
- List the local registered content files (L)
- List the on-line registered content files (O)
'''
import socket                   # Import socket module
from collections import namedtuple
import select
import pickle

s = socket.socket(socket.SOCK_DGRAM)             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
# client is connected to the server
# define the PDU
PDU = namedtuple('UDP', ['data_type', 'data'])

################## Functions
def select_name():
    return input('Please enter preferred username:')

def de_register(s,username, filename):
    t_pdu = PDU('T',{'peer_name':username,'file_name':filename})
    b_t_pdu = pickle.dumps(t_pdu)
    s.send(b_t_pdu)
    b_conf_pdu = s.recv
    conf_pdu = pickle.loads(b_conf_pdu)
    if conf_pdu.data_type == 'A':
        print('successfully removed from the list')

    elif conf_pdu.data_type == 'E':
        print(conf_pdu.data)

    # return conf_pdu


def download_file(file_name, address, destination):
    ip = address[0]
    port_number = address[1]
    ds = socket.socket()
    ds.connect((ip,port_number))
    # establish new TCP connection
    pdu = PDU('D',file_name)
    b_pdu = pickle.dumps(pdu)
    # create a 'D' type pdu asking for the file
    ds.send(b_pdu)
    # send pdu to peer address (destination)
    r_b_pdu = ds.recv()
    r_pdu = pickle.loads(r_b_pdu)
    data_type = r_pdu.data_type
    if data_type == 'E':
        print('File does not exist anymore')
    elif data_type == 'C':
        with open(destination+file_name) as f:
            f.write(r_pdu.data)
    # receive the data
    # it should be 'C' type
    # write to the file

##################


# select username
username = select_name()

# create a server to listen to the file requests
'''
Here we config the server capability of the peers. As a server we need to specify ip address and ports. Since all the 
peers are inside the local network (IP=127.0.0.1), we need to use unique port numbers for each peers so they can
bind socket successfully. This can be done by generating random numbers and using try/except command to bind a socket.
Withing multiple attempt we can be sure that peer would eventually bind a socket with random port number. Here I do not
use this approach. Instead I asked the user to enter a port number manually. During the test, for each of the peers,
you will need to enter different port numbers for different peers. 
The '' for IP address means our server is listening to all IPs,
you can change it to socket.hostname instead like before.
'''
inputs = []
outputs = []
exp = []
ss = socket.socket() # this is a TCP connection
serverPort = int(input('Please enter listening port number for the download server:'))
try:
    ss.bind(('',serverPort))
except Exception:
    pass
ss.listen(5)
inputs.append(ss)
exp.append(ss)

# service loop
while True:
    readable, writable, exceptional = select.select(inputs, outputs, exp)
    for sock in readable: # check the incoming connection requests
        if sock is ss:
            fileReq_Socket, fileReq_addr = ss.accept() # accept connection
            ss.recv() # receive the request
            # check the file name (it should be 'D' type)
            # send the file using 'C' type
            # if file doest not exist send 'E' pdu

    else: # there is no incoming connection request, so go to the menu and ask the user for command

        command = str(input('Please choose from the list below:\n'
                             '[O] Get online list\n'
                             '[L] List local files\n'
                             '[R] Register a file\n'
                             '[T] De-register a file\n'
                             '[Q] Quit the program\n'))

        if command == 'O':
            # send 'O' type pdu
            # receive the list
            # print the list
            # ask user for the target file
            # create 'S' type pdu
            # send 'S' pdu to the index server
            # receive 'S' pdu in response
            # extract address
            # establish new connection to the peer
            destination = './'
            download_file(file_name, address, destination)

        if command == 'L':
            # list local files

        if command == 'R':

            filename = input('Please enter file name to be registered: ')

            # get the file name
            # create 'R' pdu using username, filename, IPaddress and portnumber
            # send 'R' pdu
            # receive response pdu
            # if 'A', done
            # else if 'E',
                while pdu.data_type == 'E': # a used may need to retry multiple times to register a username on server!
                    # ask user to change username
                    username = select_name()
                    # send 'R' pdu
                    # receive response
                    # extract data_type

        if command == 'T': # De-register file from index server
            # get the file name from user and de-register it from the index server
            de_register(username, input('Please enter file name: '))



        if command == 'Q':
            # for all the registered files:
            for all file_names:
                de_register(username, filename)
            # quit the program
            s.close()
