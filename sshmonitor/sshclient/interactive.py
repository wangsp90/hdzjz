import socket
import sys
from paramiko.py3compat import u
def windows_shell(chan):
    import threading

    sys.stdout.write(
        "Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n"
    )

    def writeall(sock):
        while True:
            data = sock.recv(256).decode("utf-8")
            if not data:
                sys.stdout.write("\r\n*** EOF ***\r\n\r\n")
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()
    #启动后台线程，一直监控输出
    writer = threading.Thread(target=writeall, args=(chan,)) 
    writer.start()

    try:
        while True:
            d = sys.stdin.readline()
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass