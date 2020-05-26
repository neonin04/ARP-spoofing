import socket

HOST = '192.168.0.13'
PORT = 9999

# 주소 체계  IPv4, 소켓 타입 TCP 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 포트 사용중이라 연결할 수 없다는 WinError 10048 에러 해결를 위해 필요
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind 함수에 (ip, port) 튜플 전달
# HOST는 hostname, ip address, 빈 문자열 ''이 될 수 있다.
# 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용
# PORT는 1-65535 사이의 숫자를 사용할 수 있다.
server_socket.bind((HOST, PORT))

# 총 1개의 동시접속을 허용. 입력하지 않을 시 파이썬이 자의적으로 판단
server_socket.listen(1)

# accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓과 클라이언트의 AF를 반환
connection_socket, addr = server_socket.accept()
print('Connected by', addr)

i=10
# 무한루프를 돌면서
while True:

    # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다.
    recv_msg = connection_socket.recv(1024) #1024바이트
    print('Received from: ', addr, recv_msg.decode('utf-8'))

    # 메시지 전송
    send_msg = input("Sending: ")
    connection_socket.send(send_msg.encode('utf-8'))

    i = i-1
    if i == 0:
        break

# 소켓을 닫습니다.
connection_socket.close()
server_socket.close()
