import socket
import time
from playsound import playsound
import threading
import os
import winsound

is_playing = False
stop_event = threading.Event()


def initialize_server(host, port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(1)
    return serversocket

def main():
    host = socket.gethostbyname(socket.gethostname())#'192.168.68.101'  # Your PC's local IP address
    port = 49152  # Define the port to listen on
    serversocket = initialize_server(host, port)

    try:
        print(f"PC Server listening on {host}:{port}")
        while True:
            (clientsocket, address) = serversocket.accept()
            print(f"Connection established from {address}")

            # Receive data from the connected client (server)
            data = clientsocket.recv(1024).decode()

            # Check if received data indicates an alarm activation
            if data == "ACTIVATE_ALARM":
                print("Received command to activate the alarm!")
                # Add your logic here to trigger the alarm on the PC
                play_audio(data)
            elif data == "DEACTIVATE_ALARM":
                print("Received command to deactivate the alarm!")
                # Add your logic here to trigger the alarm on the PC
                play_audio(data)

    except KeyboardInterrupt: 
        print("\nShutting down...\n")
    except Exception as exc:
        print("Error:\n")
        print(exc)
    finally:
        serversocket.close()

def play_audio(command):
    global is_playing, audio_thread

    script_directory = os.path.dirname(os.path.abspath(__file__))
    audio_file_path = os.path.join(script_directory, "alarm.mp3")


    if command == "ACTIVATE_ALARM" and not is_playing:
        is_playing = True
        audio_thread = threading.Thread(target=loop_audio, args = (audio_file_path,))
        audio_thread.start()
        print("Audio activated.", is_playing)
    elif command == "DEACTIVATE_ALARM" and is_playing:
        is_playing = False
        stop_event.set()
        audio_thread.join()
        print("Audio deactivated.", is_playing)
    else:
        print("Invalid command.")

def loop_audio(audio_file_path):
    global is_playing
    audiofile = "file:///c:/Users/Cliff/linux/AlarmProject/alarm.mp3"
    try:
        playsound(audiofile, block=False)
        while not stop_event.is_set():
            logger("Thread activated\n")
            time.sleep(0.1)
        stop_event.set()
        audio_thread.join()
    except Exception as e:
        logger(e)
    
def logger(message):
    print(message)


if __name__ == "__main__":
    main()

