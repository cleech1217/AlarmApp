import socket
from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange
import time

# Define the service type to discover
SERVICE_TYPE = "_myservice._tcp.local."

# Initialize Zeroconf
zeroconf = Zeroconf()

# Function to handle service discovery
class MyListener:
    def __init__(self):
        self.server_info = None

    def remove_service(self, zeroconf, service_type, name):
        pass

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        if info:
            self.server_info = info

    def update_service(self, zeroconf, service_type, name):
        pass

# Discover services
listener = MyListener()
browser = ServiceBrowser(zeroconf, SERVICE_TYPE, listener)

# Wait for the server info to be discovered
while listener.server_info is None:
    pass

# Extract the server address and port from the discovered info
server_addresses = [socket.inet_ntoa(addr) for addr in listener.server_info.addresses]
server_port = listener.server_info.port

# Use the first discovered address (you can modify this logic if there are multiple addresses)
server_address = server_addresses[0] if server_addresses else None

if server_address:
    print(f"Discovered Server Address: {server_address}")
    print(f"Discovered Server Port: {server_port}")
else:
    print("No server address found. Exiting.")
    exit()

# Function to send a command to the server
def send_command(command):
    try:
        # Create a socket to connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_address, server_port))

        # Send the command to the server
        client_socket.send(command.encode('utf-8'))

        # Receive and print the server's response
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server Response: {response}")

        # Close the client socket
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    """while True:
        # Input a command from the user
        command = input("Enter a command (or 'exit' to quit): ")
        if command.lower() == 'exit':
            break

        # Send the command to the discovered server
        send_command(command)
    """
    test_command = ["Alarm Status", "Activate", "Deactivate"]

    for test in test_command:
        send_command(test)
        time.sleep(1)
        send_command(test_command[0])
        time.sleep(3)

# Clean up Zeroconf
zeroconf.close()
