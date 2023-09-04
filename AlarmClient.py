import socket
import os
import threading
import time
import logging
from playsound import playsound
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import json


# Constants
HOST = socket.gethostbyname(socket.gethostname())
PORT = 49152
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
AUDIO_FILE_PATH = os.path.join(SCRIPT_DIRECTORY, "alarm.mp3")

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Thread control
is_playing = False
stop_event = threading.Event()
audio_thread = None

def initialize_server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, PORT))
    serversocket.listen(1)
    return serversocket

def do_something():
    global is_playing
    
    try:
        while not stop_event.is_set():
            logger.info("Try playing audio: " + AUDIO_FILE_PATH)
            #playsound(AUDIO_FILE_PATH)
            logger.info("Playing audio: " + AUDIO_FILE_PATH)
            time.sleep(5)
    except Exception as e:
        logger.error(e)
    finally:
        logger.info("Playback complete.")
        is_playing = False

def start_thread():
    global audio_thread, is_playing

    if is_playing:
        logger.info("Thread is already running.")
        return
    is_playing = True
    audio_thread = threading.Thread(target=do_something)
    audio_thread.start()
    logger.info("Thread started.")

def stop_thread():
    global audio_thread, is_playing
    if audio_thread and audio_thread.is_alive():
        stop_event.set()
        audio_thread.join()
        logger.info("Thread stopped.")
        stop_event.clear()
        is_playing = False
    else:
        logger.info("Thread is not running.")

def get_current_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    logger.info("Getting current volume: ")
    return int(volume.GetMasterVolumeLevelScalar() * 100)

def set_volume(left_volume, right_volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Set the left and right channel volumes
    volume.SetChannelVolumeLevelScalar(0, left_volume, None)  # 0 for left channel
    volume.SetChannelVolumeLevelScalar(1, right_volume, None)  # 1 for right channel

def main():
    serversocket = initialize_server()
    try:
        logger.info(f"PC Server listening on {HOST}:{PORT}")
        while True:
            (clientsocket, address) = serversocket.accept()
            logger.info(f"Connection established from {address}")

            data = clientsocket.recv(1024).decode()
            logger.info(("Received command: ", data))
            check_command(data)

            alarm_status = "Alarm Activated" if is_playing else "Alarm Deactivated"
            clientsocket.sendall(json.dumps(alarm_status).encode())
            logger.info("Sending reply: " + json.dumps(alarm_status))
            clientsocket.close()  # Close the client socket
    except KeyboardInterrupt:
        logger.info("\nShutting down...\n")
    except Exception as exc:
        logger.error("Error:\n", exc)
    finally:
        serversocket.close()

def check_command(command):
    if command == "ACTIVATE_ALARM":
        start_thread()
    elif command == "DEACTIVATE_ALARM":
        stop_thread()
    else:
        logger.info("Requesting Status...")

if __name__ == "__main__":
    main()
