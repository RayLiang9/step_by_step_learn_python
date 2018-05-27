#-*- coding:utf-8 _*-
"""
author: iceman
"""

import time
import socket

COMMAND = 'timetampe'

def start_server(host, port):
    #1. 创建socket句柄
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
        if int(port) >0: #端口必须大于零
            addr = (host, port)
            tcp_server.bind(addr) #2. 绑定端口，参数为ip:port元组
            tcp_server.listen(10) #3. 开始监听端口，
            while True: #4.
                print('*'*10 + 'now waiting for client connect' + '*'*10)
                tcp_client, client_addr = tcp_server.accept() #5. 等待客户端连接
                print('new client : %s' % client_addr[0] + ':' + str(client_addr[1]))
                recv_data = tcp_client.recv(1024) #6.1 从客户端获取命令
                recv_data = str(recv_data, encoding='utf-8')
                if recv_data == COMMAND: #是否匹配命令
                    current_timestamp = time.ctime() #获取当前时间
                    tcp_client.send(bytes(current_timestamp, 'utf-8')) #6.2 返回当前时间给客户端
                tcp_client.close() #7. 关闭socket句柄
    #8. 此处使用with语句，超出作用于自动释放

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 8099
    start_server(HOST, PORT)