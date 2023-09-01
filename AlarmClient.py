from socket import *
import socket
from playsound import playsound
import threading
import os
from ctypes import cast, POINTER

is_playing = False
stop_event = threading.Event()
audio_lock = threading.Lock()
audio_thread = None
host = socket.gethostbyname(socket.gethostname())#'192.168.68.101'  # Your PC's local IP address
port = 49152  # Define the port to listen on

def initialize_server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(1)
    return serversocket

def main():

    serversocket = initialize_server()

    try:
        print(f"PC Server listening on {host}:{port}")
        while True:
            (clientsocket, address) = serversocket.accept()
            print(f"Connection established from {address}")

            # Receive data from the connected client (server)
            data = clientsocket.recv(1024).decode()
            logger(("Recieved command: ", data))
            check_command(data)

            # Send reply, server status and alarm status
            if is_playing: alarmstatus = "Alarm Activated" 
            else: alarmstatus = "Alarm Deactivated"
            clientsocket.sendall(alarmstatus.encode())
            logger(("Sending reply: ", alarmstatus))
            clientsocket.shutdown(SHUT_WR)

    except KeyboardInterrupt: 
        print("\nShutting down...\n")
    except Exception as exc:
        print("Error:\n")
        print(exc)
    finally:
        serversocket.close()

def check_command(command):
    global is_playing, audio_thread

    script_directory = os.path.dirname(os.path.abspath(__file__))
    audio_file_path = os.path.join(script_directory, "alarm.mp3")
    #audio_file_path = "/alarm.mp3"

    with audio_lock:
        if command == "ACTIVATE_ALARM" and not is_playing:
            is_playing = True
            audio_thread = threading.Thread(target=loop_audio, args=(audio_file_path,))
            audio_thread.start()
            print("Audio activated.", is_playing)
        elif command == "DEACTIVATE_ALARM" and is_playing:
            is_playing = False
            stop_event.set()  # Set the event to signal thread to stop
            stop_event.clear() 
            print("Audio deactivated.", is_playing)
        #else:
        #    print("Invalid command.")

def loop_audio(audio_file_path):
    global is_playing


    try:
        while not stop_event.is_set():
            logger("Try playing audio: " + audio_file_path)
            playsound(audio_file_path)
            logger("Playing audio: " + audio_file_path)
        logger("Playback complete.")
        #print("Restoring volume...")
        #controller.restore_volume()
        #volume.SetMasterVolumeLevelScalar(volume, None)
        stop_event.clear() 
    except Exception as e:
        logger(e)
    
def logger(message):
    print(message)

if __name__ == "__main__":
    main()

    """
    #controller = AudioVolumeController()
    #controller.get_default_volume()
    #print("default volume: "+ controller.default_volume.to_bytes)
    #controller.set_max_volume()
    #print("default volume: ")
    """

"""class AudioVolumeController:
    def __init__(self):
        self.default_volume = 1
    
    def get_default_volume(self):
        # Get the default audio output device volume
        default_device = ctypes.c_int()
        ctypes.windll.winmm.waveOutGetVolume(None, ctypes.byref(default_device))
        self.default_volume = default_device.value
        
    def set_max_volume(self):
        # Set both left and right channels to maximum volume (0xFFFF)
        max_volume = 0xFFFF
        ctypes.windll.winmm.waveOutSetVolume(None, max_volume)
    
    def restore_volume(self):
        # Restore the previous audio output device volume
        ctypes.windll.winmm.waveOutSetVolume(None, self.default_volume)
"""