from socket import *
import sys
import time

#具体功能
class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd=sockfd
    
    def do_list(self):
        self.sockfd.send(b'L')#发送请求
        #等待回复
        data=self.sockfd.recv(128).decode()
        if data=='OK':
            data=self.sockfd.recv(4096).decode()
            files=data.split(',')
            for f in files:
                print(f)
        else:
            #无法完成操作
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit('谢谢使用')

    def do_get(self,filename):
        self.sockfd.send(('G '+filename).encode())
        data=self.sockfd.recv(128).decode()
        if data=='OK':
            fd=open(filename,'wb')
            while True:
                data=self.sockfd.recv(1024)
                if data==b'##':
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self,filename):
        self.sockfd.send(('P '+filename).encode())
        data=self.sockfd.recv(128).decode()
        if data=='OK':
            fd=open(filename,'rb')
            while True:
                data=fd.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            fd.close()
        else:
            print(data)

#网络连接
def main():
    sockfd=socket()
    try:
        sockfd.connect(('127.0.0.1',12580))
    except Exception as e:
        print('连接服务器失败：',e)
        return

    #创建文件处理类对象
    ftp=FtpClient(sockfd)#sockfd变成属性

    while True:
        print('\n-------命令选项--------')
        print('***    1.list       ***')
        print('***    2.get file   ***')
        print('***    3.put file   ***')
        print('***    quit         ***')
        print('-----------------------')
        #收发消息
        cmd=input('输入命令>>')
        if cmd.strip()=='1':
            ftp.do_list()
        elif cmd=='2':
            f=input('文件名：')
            filename=f.strip().split(' ')[-1]
            ftp.do_get(filename)
        elif cmd=='3':
            f=input('文件名：')
            filename=f.strip().split(' ')[-1]
            ftp.do_put(filename)
        elif cmd=='quit':
            ftp.do_quit()
        else:
            print('请输入正确命令') 
        # data=sockfd.recv(1024)
        # print('From server:',data.decode())

    sockfd.close()

if __name__=="__main__":
    main()