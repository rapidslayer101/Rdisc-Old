from socket import *
from threading import Thread
import time

startTime = time.time()

if __name__ == '__main__':
    target = input('Enter the host to be scanned: ')
    t_IP = gethostbyname(target)
    print('Starting scan on host: ', t_IP)

    for i in range(0, 25565):
        def check(i):
            s = socket(AF_INET, SOCK_STREAM)
            conn = s.connect_ex((t_IP, i))
            if (conn == 0):
                print('Port %d: OPEN' % (i,))
            s.close()
        Thread(target=check, args=(i,)).start()
print('Time taken:', time.time() - startTime)