import socket
from tkinter import W
import msvcrt
def SendCommand(Commands):
    msgFromClient = Commands
    if not Commands in ['a','w','d']:
        return
    bytesToSend = str.encode(msgFromClient)

    serverAddressPort = ('LAPTOP-2DSKFU1D', 20001)

    bufferSize = 1024

    # Create a UDP socket at client side

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    UDPClientSocket.connect(serverAddressPort)
    UDPClientSocket.send(bytesToSend)
while(True):
    SendCommand(msvcrt.getch().decode())
