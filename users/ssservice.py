import socket

class ssService:
    def __init__(self,ip,port,timeout):
        self.host = (ip,port)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)

    def cmd(self,msg):
        try:
            self.sock.sendto(msg, self.host)
            data, addr = self.sock.recvfrom(1024)
        except Exception: 
            return "ERR"
        return data

    def close(self):
        self.sock.close()
