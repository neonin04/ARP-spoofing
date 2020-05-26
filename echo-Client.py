import socket

# 서버의 주소
HOST = '192.168.0.13'
# 서버에서 지정해 놓은 포트 번호
PORT = 9999

# 주소 체계  IPv4, 소켓 타입 TCP 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 지정한 HOST와 PORT를 사용하여 서버에 접속
client_socket.connect((HOST, PORT))

while True:

    # 메시지 전송
    send_msg = input("Sending: ")
    client_socket.send(send_msg.encode('utf-8'))

    # 메시지 수신
    recv_msg = client_socket.recv(1024)
    print('Received: ', recv_msg.decode('utf-8'))

# 소켓을 닫습니다.
client_socket.close()
