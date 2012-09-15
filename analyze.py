import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Text file to read from and write to')
    args = parser.parse_args()

    filename = 'primes.txt'
    if not args.file == None:
        filename = args.file

    primefile = open(filename, 'r')
    primes = []

    sys.stdout.write('Reading file... ')
    sys.stdout.flush()
    for line in primefile:
        primes.append(int(line))
    sys.stdout.write('Done\n')
    sys.stdout.flush()

    primefile.close()
    diff = 0.0

    sys.stdout.write('Summing Differences... ')
    sys.stdout.flush()
    for i in range(len(primes) - 1):
        diff += primes[i+1] - primes[i]
    sys.stdout.write('Done\n')
    sys.stdout.flush()

    diff = diff / len(primes)

    sys.stdout.write('Average Diff: ' + str(diff) + '\n')

if __name__ == '__main__':
    main()
