from socket import *

def initializeServer(port):
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind(('192.168.68.101', port))
    serversocket.listen(5)
    print(f"Server listening on port {port}")
    return serversocket

def main():
    port = 49152  # Define the port to listen on
    serversocket = initializeServer(port)

    try:
        while True:
            (clientsocket, address) = serversocket.accept()
            print(f"Connection established from {address}")

            # Receive data from the connected client (phone)
            data = clientsocket.recv(1024).decode()
            print(data)

            # Check if received data indicates an alarm trigger
            if "ACTIVATE_ALARM" in data:
                print("Alarm triggered! Sending command to PC...")
                # Simulate sending a command to activate the alarm on the PC
                pc_address = ('192.168.68.101', 49153)  # Replace with the actual PC address
                pc_socket = socket(AF_INET, SOCK_STREAM)
                pc_socket.connect(pc_address)
                print("Sending message: "+data)
                pc_socket.sendall(data.encode())
                pc_socket.close()
                

    except KeyboardInterrupt:
        print("\nShutting down...\n")
    except Exception as exc:
        print("Error:\n")
        print(exc)
    finally:
        serversocket.close()

if __name__ == "__main__":
    main()

"""
Link speed (Receive/Transmit):	1000/1000 (Mbps)
Link-local IPv6 address:	fe80::d474:7656:40f4:fd17%12
IPv4 address:	192.168.68.101
IPv4 DNS servers:	192.168.254.254
192.168.68.1
Manufacturer:	Intel Corporation
Description:	Intel(R) Ethernet Connection (2) I219-V
Driver version:	12.17.10.8
Physical address (MAC):	88-88-88-88-87-88
"""
