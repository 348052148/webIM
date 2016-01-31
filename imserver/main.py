# _*_ coding:utf-8 _*_
__author__ = 'Patrick'


import socket
import threading
import sys
import os
import base64
import hashlib
import struct
import time
import json
import sqlite3
from user import *

# ====== config ======
HOST = 'localhost'
PORT = 3368
MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
HANDSHAKE_STRING = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n" \
                   "Connection: Upgrade\r\n" \
                   "Sec-WebSocket-Accept: {1}\r\n" \
                   "WebSocket-Location: ws://{2}/chat\r\n" \
                   "WebSocket-Protocol:chat\r\n\r\n"
connlist=list()
'''
命令符。
>id 表示单播发送消息给具体好友
<groupid 广播发送消息给一组好友
@ 初始化信息命令
& 登录
$ 搜索
! 添加好友
^ 退出
0 命令符 1 命令参数 2 数据 服务端到客户端
0 命令符 1 命令参数 2 数据 客户端到服务端
'''
class Th(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.con = connection

    def run(self):
        #返回数据 用户验证
        print('------->')
        u=User()
        while True:
            data=self.recv_data(1024)
            print(data)
            dic=str(data).split("_")
            if dic[0] == '^':
                exit()
            elif dic[0] == '&':
                if u.find(dic[2]):
                    if u.pw == dic[3]:
                        u.updateUserStat(1);
                        self.send_data('&_1_welcom to im');
                        break
                else:
                    self.send_data('&_0_user login err');

        #初始化用户信息
        user=userInfo(u.name,u.uid,1000,1,u.getFriends(),self.con)
        connlist.append(user)
        #封装用户信息 并发送
        dc={'name':user.name,'uid':user.uid,'gid':user.gid,'friend':user.friend}
        self.send_data('@_welcomto_'+json.dumps(dc))
        #接受消息并发送
        while True:
            data=self.recv_data(1024)
            #命令解析
            dic=str(data).split("_")
            cmd=dic[0]
            id=dic[1]
            d=dic[2]
            if cmd == '>':
                for conn in connlist:
                    print('--->单播')
                    if conn.uid == int(id):# or conn.uid == user.uid:
                        timels=time.strftime('%Y-%m-%d %X',time.gmtime(time.time()))
                        send_data('>_'+user.name+'_'+str(d)+'_'+timels+'_'+str(user.uid),conn.conn)
            elif cmd == '<':
                for conn in connlist:
                    print('--->广播')
                    timels=time.strftime('%Y-%m-%d %X',time.gmtime(time.time()))
                    send_data(conn.name+'_'+str(d)+'_'+timels,conn.conn)
            elif cmd == '$':
                print('---->搜索')
                doc=u.searchFriend(d);
                self.send_data('$_search_'+json.dumps(doc))
            elif cmd == '!':
                print('--->添加好友')
                stat=u.addFriend(dic[2],dic[3])
                self.send_data('!_'+json.dumps(stat))
            elif cmd == '^':
                u.updateUserStat(0)
                print(len(connlist))
                connlist.remove(user)
                print(len(connlist))
                break;
            else:
                for conn in connlist:
                    timels=time.strftime('%Y-%m-%d %X',time.gmtime(time.time()))
                    send_data(conn.name+'_'+str(d)+'_'+timels,conn.conn)
        print(user.name+'退出')
        self.con.close()

    def recv_data(self, num):
        print('---------recv')
        try:
            all_data = self.con.recv(num)
            print(all_data)
            if not len(all_data):
                print('wu')
                return False
        except:
            return False
        else:
            #code_len = ord(all_data[1]) & 127
            code_len = all_data[1] & 127
            if code_len == 126:
                masks = all_data[4:8]
                data = all_data[8:]
            elif code_len == 127:
                masks = all_data[10:14]
                data = all_data[14:]
            else:
                masks = all_data[2:6]
                data = all_data[6:]
            raw_str = ""
            i = 0
            for d in data:
                raw_str += chr(d ^ masks[i % 4])
                i += 1
            print(type(raw_str))
            return raw_str

    # send data
    def send_data(self, data):
        if data:
            data = str(data)
        else:
            return False
        print('--->'+data)
        token = b"\x81"
        length = len(data)
        if length < 126:
            token += struct.pack("B", length)
        elif length <= 0xFFFF:
            token += struct.pack("!BH", 126, length)
        else:
            token += struct.pack("!BQ", 127, length)
        #struct为Python中处理二进制数的模块，二进制流为C，或网络流的形式。
        print(token)
        #data = '%s%s' % (token.decode(), data)
        print(data)
        self.con.send(token+data.encode())
        return True
    def sends(self,data):
        print("send..")
        first_byte = '\x00'
        print(type(first_byte))
        payload = data.encode('utf-8')
        pl = first_byte.encode() + payload + '\xFF'.encode()
        self.con.send(pl)
#recv data
def recv_data(num,conn):
    print('---------recv')
    try:
        all_data = conn.recv(num)
        print('=')
        if not len(all_data):
            print('wu')
            return False
    except:
        return False
    else:
        print(type(all_data))
            #code_len = ord(all_data[1]) & 127
        code_len = all_data[1] & 127
        if code_len == 126:
            masks = all_data[4:8]
            data = all_data[8:]
        elif code_len == 127:
            masks = all_data[10:14]
            data = all_data[14:]
        else:
            masks = all_data[2:6]
            data = all_data[6:]
        raw_str = ""
        i = 0
        for d in data:
            raw_str += chr(d ^ masks[i % 4])
            i += 1
        print(type(raw_str))
        return raw_str
#
# send data
def send_data(data,conn):
    if data:
        data = str(data)
    else:
        return False
    print('--->'+data)
    token = b"\x81"
    length = len(data)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)
        #struct为Python中处理二进制数的模块，二进制流为C，或网络流的形式。
    print(token)
        #data = '%s%s' % (token.decode(), data)
    print(data)
    print(data.encode())
    conn.send(token+data.encode())
    return True
# handshake 处理握手
def handshake(con):
        headers = {}
        shake = con.recv(1024)

        if not len(shake):
            return False
        shake=shake.decode()
        header, data = shake.split('\r\n\r\n', 1)
        for line in header.split('\r\n')[1:]:
            key, val = line.split(': ', 1)
            headers[key] = val

        if 'Sec-WebSocket-Key' not in headers:
            print ('This socket is not websocket, client close.')
            con.close()
            return False

        sec_key = headers['Sec-WebSocket-Key']
        print(type(sec_key))
        print(type(MAGIC_STRING))
        res_key = base64.b64encode(hashlib.sha1(sec_key.encode() + MAGIC_STRING.encode()).digest())
        print(type(res_key))
        str_handshake = HANDSHAKE_STRING.replace('{1}', res_key.decode()).replace('{2}', HOST + ':' + str(PORT))
        print (str_handshake)
        con.send(bytes(str_handshake.encode()))
        return True

def new_service():
    """start a service socket and listen
    when coms a connection, start a new thread to handle it"""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((HOST, 3368))
        sock.listen(1000)
        #链接队列大小
        print ("bind 3368,ready to use")
    except:
        print("Server is already running,quit")
        sys.exit()

    while True:
        connection, address = sock.accept()
        #返回元组（socket,add），accept调用时会进入waite状态
        print ("Got connection from ", address)
        if handshake(connection):
            print ("handshake success")
            try:
                t = Th(connection)
                t.start()
                print ('new thread for client ...')
            except:
                print ('start new thread error')
                connection.close()


if __name__ == '__main__':
    new_service()

##设计原则：
##1.主动发送一次数据，用以初始化
##2.每次send 携带额外信息，用以更新用户状态
##3.recv 接受的数据表示不同的含义，命令。信息。数据