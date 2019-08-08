import os
import sys
import time
import ipaddress
import subprocess
from tabulate import tabulate

cmd = 'ping -c 2 -i 1'
hosts = ['ya.ru', '10.1.1.1', '15.212.111.51', '64.233.162.139']
rng = ['10.1.1.1', '10.1.1.5']


def host_ping(arr):
    for host in arr:
        with open(os.devnull, 'w') as devnull:
            ping = subprocess.call(cmd.split() + [host], stdout=devnull)
            if ping == 0:
                print(f'{host} is available')
            else:
                print(f'{host} is unavailable')


def host_range_ping(arr):
    start = int(arr[0].split('.')[3])
    end = int(arr[1].split('.')[3]) + 1
    template = ''.join(arr[0][:-1])
    
    for i in range(start, end):
        address = template + str(i)
        
        with open(os.devnull, 'w') as devnull:
            ping = subprocess.call(cmd.split() + [address], stdout=devnull)
            if ping == 0:
                print(f'{address} is available')
            else:
                print(f'{address} is unavailable')


def host_range_ping_tab(arr):
    result = {'available': [], 'unavailable': []}
    start = int(arr[0].split('.')[3])
    end = int(arr[1].split('.')[3]) + 1
    template = ''.join(arr[0][:-1])
    
    for i in range(start, end):
        address = template + str(i)
        
        with open(os.devnull, 'w') as devnull:
            ping = subprocess.call(cmd.split() + [address], stdout=devnull)
            if ping == 0:
                result.get('available').append(address)
            else:
                result.get('unavailable').append(address)
    print(tabulate(result, headers='keys'))


def run_client():
    r_client = 'python -m client --mode r'
    w_client = 'python -m client --mode w'
    
    r_process = subprocess.Popen('fab client:r', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, \
            cwd="/Users/kirill/Coding/school/client-server-apps")
    out = r_process.stdout.read()
    print(out)

    w_process = subprocess.Popen("fab client:w", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, \
        cwd="/Users/kirill/Coding/school/client-server-apps")
    w_process.stdin.write('jon\necho\ntest'.encode())
    print(w_process.communicate())


def run_clients(num):
    r_client = 'python -m client --mode r'
    w_client = 'python -m client --mode w'
    
    for i in range(num):
        r_process = subprocess.Popen('fab client:r', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, \
                cwd="/Users/kirill/Coding/school/client-server-apps")
        out = r_process.stdout.read()
        print(out)

        w_process = subprocess.Popen("fab client:w", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, \
            cwd="/Users/kirill/Coding/school/client-server-apps")
        w_process.stdin.write('jon\necho\ntest'.encode())
        print(w_process.communicate())


# host_ping(hosts)
# host_range_ping(rng)
# host_range_ping_tab(rng)
# run_client()
run_clients(2)