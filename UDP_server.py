import socket

#ソケット作成
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    #接続待ちをするIPアドレスとポート番号を指定
    s.bind(('127.0.0.1', 50007))
    while True:
        #受信したメッセージをバッファー buf に格納する
        data, addr = s.recvfrom(1024)
        print("data: {}, addr: {}".format(data, addr))