import socket
import threading
import time
from zeroconf import ServiceInfo, Zeroconf
import playAlarm
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the service name and port
SERVICE_NAME = "Alarm Service"
PORT = 12345

# Initialize Zeroconf
zeroconf = Zeroconf()

# Create and register the service with properties
properties = {
    "description": "My Service Description",
    "path": "/my-service-path",
}
 #[socket.inet_pton(socket.AF_INET, socket.gethostbyname(socket.gethostname()))],
 #socket.inet_pton(socket.AF_INET, '127.0.0.1'),
info = ServiceInfo("_http._tcp.local.",
                   f"{SERVICE_NAME}._http._tcp.local.",
                   addresses=[socket.inet_pton(socket.AF_INET, socket.gethostbyname(socket.gethostname()))],
                   port=PORT,
                   properties=properties)

zeroconf.register_service(info)

# Function to handle incoming connections and commands
def handle_connection(client_socket):
    while True:
        try:
            # Receive the command from the client
            command = client_socket.recv(1024).decode('utf-8')
    
            if not command:
                break
            
            # Handle the command and send a response
            if command == 'Alarm Status':
                #set alarm status
                if playAlarm.is_playing:
                    response = "Active"
                else:
                    response = "Inactive"
            elif command == 'Activate':
                #Activate alarm
                playAlarm.start_thread()
                response = 'Active'
            elif command == 'Deactivate':
                #Deactivate alarm
                playAlarm.stop_thread()
                response = 'Inactive'
            else:
                response = 'Unknown Command'
            
            # Send the response back to the client
            client_socket.send(response.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error: {e}")
            break


def main():
    # Create a socket to listen for incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(5)

    print(f"Listening for connections on port {PORT}...")
    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            
            # Handle the connection in a new thread
            client_thread = threading.Thread(target=handle_connection, args=(client_socket,))
            client_thread.start()

            time.sleep(5) # Battery/CPU optimization
           
    except Exception as e:
        logger.info(e)

if __name__ == "__main__":
    main()
