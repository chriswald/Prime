import argparse
import signal
import sys
import time

# Globals
signaled = False
initprimes = 0
tnow = time.time()
tthen = tnow
numprimes_str = '0'

def signal_handler(signal, frame):
    global signaled
    signaled = True

def read_file(filename):
    global initprimes
    global numprimes_str
    primes = []
    try:
        fin = open(filename, 'r')
        for line in fin.readlines():
            primes.append(int(line))
        fin.close()
        initprimes = len(primes)
    except IOError:
        primes.append(2)
    numprimes_str = str(len(primes))
    return primes

def phun():
    sys.stdout.write('=')
    sys.stdout.flush()

def ptho_write(primes, filename):
    fout = open(filename, 'a')
    for p in primes[-1000:]:
        fout.write(str(p) + '\n')
    fout.close()

def ptho_time():
    global tnow
    global tthen

    tnow = time.time()
    elapsed = tnow - tthen
    persec = 1000 / elapsed
    tthen = tnow
    return str(persec) + ' primes/sec '

def ptho_print(primes):
    global numprimes_str
    time_str = ptho_time()
    
    sys.stdout.write('] ' + time_str)
    for i in range(len(time_str) + 2):
        sys.stdout.write('\b')
    for i in range(len(numprimes_str) + 13):
        sys.stdout.write('\b')
    for i in range(len(numprimes_str) + 13):
        sys.stdout.write(' ')
    for i in range(len(numprimes_str) + 13):
        sys.stdout.write('\b')
    numprimes_str = str(len(primes))
    sys.stdout.write(numprimes_str + ': [')
    sys.stdout.flush()

def ptho(primes, filename):
    ptho_write(primes, filename)
    ptho_print(primes)

def find_primes(primes, filename):
    index = primes[-1] + 1

    while not signaled:
        isprime = True
        i = 0
        maxval = index

        while i < maxval and i < len(primes):
            maxval = index / primes[i]
            if index % primes[i] == 0 and not primes[i] == index:
                isprime = False
                break
            i += 1

        if isprime:
            primes.append(index)
            if len(primes) % 100 == 0:
                phun()
            if len(primes) % 1000 == 0:
                ptho(primes, filename)

        index += 1

    fout = open(filename, 'a')
    for p in primes[-(len(primes) % 1000):]:
        fout.write(str(p) + '\n')
    fout.close()

    sys.stdout.write('\n' + str(len(primes) - initprimes) + ' primes found.')
    sys.stdout.flush()

def main():
    sys.stdout.write('Start...\n')
    sys.stdout.flush()
    
    primes = []
    filename = 'primes.txt'

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Text file to read from and write to')
    args = parser.parse_args()

    if not args.file == None:
        filename = args.file

    primes = read_file(filename)
    
    sys.stdout.write('Beginning at ' + str(primes[-1] + 1) + ' with ' + numprimes_str + ' prime ' + ('number' if numprimes_str == '1' else 'numbers') + '.\n')
    sys.stdout.write(str(len(primes)) + ': [          ]')
    sys.stdout.write('\b\b\b\b\b\b\b\b\b\b\b') # That's 11 backspaces
    for i in range(int(len(primes) % 1000 / 100)):
        sys.stdout.write('=')
    sys.stdout.flush()

    find_primes(primes, filename)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
