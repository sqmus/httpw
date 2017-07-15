#!/bin/python
#   HTTP Witch
# Thanks for Alexandr Kozlov
import socket
import thread
import string
import select
import sys

PL = ''
RH = ''
RP = int()
LP = int()

class httpw:

    def __init__():
        pass

    def openconf(path): # on text file " Listen port | Remote Host:Remote Port | Payload "
        global PL
        global RH
        global RP
        global LP
        try:
            config = open(path,'r')
        except:
            exit()
        config = config.split('|')
        LP = config[0]
        remote = config[1].split(':')
        RH = remote[0]
        RP = remote[1]
        PL = config[2]
        print '[!] Config Loaded'
    
    def payload_subitute(payload,raw_data,remote,proto):
        puff = payload.replace('[raw]',raw_data)
        puff = puff.replace('[host]',remote[0])
        puff = puff.replace('[port]',remote[1])
        puff = puff.replace('[host_port]',(remote[0] + ':' + remote[1]))
        puff = puff.replace('[protocol]',proto)
        puff = puff.replace('[crlf]','\r\n')
        puff = puff.replace('[connect]',('CONNECT ' + (remote[0] + ':' + remote[1]) + ' ' + proto))
        puff = puff.replace('[cr]','\r')
        puff = puff.replace('[lf]','\n')
        puff = puff.replace('[lfcr]','\n\r')
        return puff

    def getproto(req):
        proc = req.find(' ',req.find(':')) + 1
        filtered = req[proc:]
        req_up = filtered.find('\r\n')
        return filtered[:req_up]

    def getremote(req):
        proc = req.find(' ') + 1
        filtered = req[proc:]
        req_up = filtered.find(' ')
        result = filtered[:req_up]
        return result.split(':')

    def getraw(req):
        return req[:req.find('\r\n')]

    def recvhttp(sock):
        count = 1
        data = sock.recv(1)
        while data.find('\r\n\r\n'.encode()) == -1:
            if not data: break
            data = data + socket.recv(1)
            count += 1
            if count > 8192 * 8: break
        return data

    def connect(csock,ssock,buffx):
        sockz = [csock,ssock]
        tmt = 0
        print "[*] Attempting to Connect .."
        while 1:
            tmt += 1
            top , mid , bot = select.select(sockz,[],sockz,3)
            if bot: break

            if top:
                for sock in top:
                    try:
                        packt = sock.recv(buffx)
                        if not packt: break;

                        if sock is ssock:
                            csock.sendall(packt)
                        else:
                            ssock.sendall(packt)

                        tmt = 0
                    except:
                        break

            if tmt == 60:break

    def threadsock(csock,caddr):
        print "[*] Bridge Esthablished @ " + caddr
        http_rq = recvhttp(csock)

        raw_data = getraw(http_rq)
        proto_ver = getproto(http_rq)
        remote_con = getremote(raw_data)
        fin_rq = payload_subtitute(PL,raw_data,remote_com,proto_ver)
        rsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        rsock.connect((RH,RP))
        rsock.sendall(fin_rq)
        rres = recvhttp(rsock)
        print "[*] \n " + getraw(rres) + " \n"
        csock.sendall(rres)
        if rres.find('200 ') != -1:
            connect(csock,rsock, 65535)

        print " [!] Connection Disbanded : " , caddr
        rsock.close()
        csock.close()
        thread.exit()
        

def main():
    print """
██╗  ██╗████████╗████████╗██████╗     ██╗    ██╗██╗████████╗ ██████╗██╗  ██╗
██║  ██║╚══██╔══╝╚══██╔══╝██╔══██╗    ██║    ██║██║╚══██╔══╝██╔════╝██║  ██║
███████║   ██║      ██║   ██████╔╝    ██║ █╗ ██║██║   ██║   ██║     ███████║
██╔══██║   ██║      ██║   ██╔═══╝     ██║███╗██║██║   ██║   ██║     ██╔══██║
██║  ██║   ██║      ██║   ██║         ╚███╔███╔╝██║   ██║   ╚██████╗██║  ██║
╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝          ╚══╝╚══╝ ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
                        Witchcraft on HTTP
                         github.com/sqmus
"""
    try:
        httpw.openconf(sys.argv[1])
    except Exception as e:
            print " [!] Usage : "+sys.argv[0]+ " < Config File >"
            exit()
    init = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    init.bind (('localhost',LP))
    init.listen(1)
    print "[*] Listening session begin .."
    while True:
        csock,caddr = init.accept()
        thread.start_new_thread(httpw.threadsock ,tuple([csock,caddr]))
    init.close()

main()
