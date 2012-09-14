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
    '''Called when ^c is pressed. Signals the program to exit.'''
    global signaled
    signaled = True

def read_file(filename):
    '''Called on program entry. Reads in all prime numbers from
    a file, or simply begins a new list of primes if the file
    cannot be opened (for example if it doesn't exist).'''
    global initprimes
    global numprimes_str
    primes = []
    try:
        fin = open(filename, 'r')
        for line in fin:
            primes.append(int(line))
        fin.close()
        initprimes = len(primes)
    except IOError:
        primes.append(2)
    numprimes_str = str(len(primes))
    return primes

def phun():
    '''Called every time 100 new primes are found.
    Writes a new character to the progress bar.'''
    sys.stdout.write('=')
    sys.stdout.flush()

def ptho_write(primes, filename):
    '''Called every time 1000 new primes are found.
    Dumps all new primes to the file. If the file
    doesn't exist it is created here.'''
    fout = open(filename, 'a')
    for p in primes[-1000:]:
        fout.write(str(p) + '\n')
    fout.close()

def ptho_time():
    '''Called every time 1000 new primes are found.
    Allows for timing how many primes are being
    found per second.'''
    global tnow
    global tthen

    tnow = time.time()
    elapsed = tnow - tthen
    persec = 1000 / elapsed
    tthen = tnow
    return str(persec) + ' primes/sec '

def ptho_print(primes):
    '''Called every time 1000 new primes are found.
    Rewrites the output string including how many
    (total) primes have been found, the progress bar
    (tracking progress to 1000 new primes), and the
    rate at which primes are being found.'''
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
    '''Calls other functions every time 1000 new
    primes are found.'''
    ptho_write(primes, filename)
    ptho_print(primes)

def find_primes(primes, filename):
    '''Main prime finding loop.'''
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

    sys.stdout.write('\n' + str(len(primes) - initprimes) + ' primes found.\n')
    sys.stdout.flush()

def main():
    '''Handles initial printing, calls file read, and calls main loop'''
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
