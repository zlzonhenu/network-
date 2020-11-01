import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    #ソケットにデータを送信する
    s.sendto(b'Hello', ('127.0.0.1', 50007))