import socket

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(('192.168.68.101', 49152))
#cmd = 'GET http://127.0.0.1/ HTTP/1.0\r\n\r\n'.encode()
cmd = 'Check Status'.encode()
mysock.send(cmd)

while True:
    data = mysock.recv(512)
    if len(data) < 1 :
        break
    print(data.decode(),end='')

mysock.close()