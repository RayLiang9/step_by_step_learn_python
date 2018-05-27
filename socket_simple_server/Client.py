#-*- coding:utf-8 _*-  
""" 
@version: 
author:iceman 
"""
import socket

COMMAND = 'timetampe'   #通过该命令获取服务器时间戳

def main(server, port):
    #1. 创建socket句柄
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_client:
        addr = (server, port)
        tcp_client.connect(addr) #2. 建立连接，此处需要一个ip:port的元组
        tcp_client.send(bytes(COMMAND, 'utf-8')) #3.1 发送命令, send需要byte数组参数
        current_timestampe = tcp_client.recv(1024) #3.2 接收服务器的响应
        if current_timestampe:
            print('current timestampe: %s' % str(current_timestampe, encoding='utf-8'))
        else:
            print('get timestampe failed')
     #4. 此处数使用with语句，超出作用于自动释放

if __name__ == '__main__':
    SERVER = '127.0.0.1'
    PORT = 8099
    main(SERVER, PORT)
