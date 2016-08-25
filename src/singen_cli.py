'''          Copyright Carlos van Rooijen 2016.
 Distributed under the Boost Software License, Version 1.0.
    (See accompanying file LICENSE or copy at
          http://www.boost.org/LICENSE_1_0.txt)
'''

#!/usr/bin/env python
#import sys
#import wave
#import math
#import struct
#import random
import argparse
#from itertools import *


from wavtools import *
from generators import *
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--channels', help="Number of channels to produce", default=2, type=int)
    parser.add_argument('-b', '--bits', help="Number of bits in each sample", choices=(16,), default=16, type=int)
    parser.add_argument('-r', '--rate', help="Sample rate in Hz", default=44100, type=int)
    parser.add_argument('-t', '--time', help="Duration of the wave in seconds.", default=60, type=int)
    parser.add_argument('-a', '--amplitude', help="Amplitude of the wave on a scale of 0.0-1.0.", default=0.5, type=float)
    parser.add_argument('-f', '--frequency', help="Frequency of the wave in Hz", default=440.0, type=float)
    parser.add_argument('filename', help="The file to generate.")
    args = parser.parse_args()

    # each channel is defined by infinite functions which are added to produce a sample.
    channels = ((sine_wave.generate(args.frequency, args.rate, args.amplitude),) for i in range(args.channels))

    # convert the channel functions into waveforms
    samples = sample_prep.compute_samples(channels, args.rate * args.time)

    # write the samples to a file
    if args.filename == '-':
        filename = sys.stdout
    else:
        filename = args.filename
    writer.write(filename, samples, args.rate * args.time, args.channels, args.bits / 8, args.rate)

if __name__ == "__main__":
    main()
