Prime.py

Copyright 2012 (c) by Christopher J. Wald

This script is designed to find prime numbers based on a method
described below. It is not the most highly optimized, but neither is
it the slowest and least optimized. The script should be exited with
^c to invoke the final file write, though fewer than 1000 primes will
be lost if exited by other means.

This file was designed with Python version 3.2 in mind, but should
work on any version that supports the Argparse module.

Usage:
	python prime.py [-f file]

	-f      The name of the file for the script to read existing
                prime numbers from and save new prime numbers to. The
                file is created if not found. If this flag is not
                provided a default name of "primes.txt" is used. This
                file can grow to be several hundred megabytes large
                and should be stored on a device that can handle
                such. The file is written to at two times. Every time
                1000 new primes are found they are dumped to the file,
                and when the script is exited any primes found since
                the last write are dumped.

Method:
	The method used to find prime numbers, in its base form, is
	rather simple. It involves simply counting from 2..N and
	dividing by 2..N-1. I have, however, applied two simple
	enhancements which both yield significant perfomance
	gains. The first is that only numbers that are already known
	to be prime are used as divisors. The second is that only
	divisors up to the square root of N are checked.
