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
import ConfigParser
import os.path
from shutil import copyfile
import collections


from wavtools import *
from generators import *
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help="The config file to be used", default='config.ini')
    parser.add_argument('filename', help="The file to generate.")
    args = parser.parse_args()
    
    if not os.path.isfile(args.config):
        print("No config found, creating one...")
        copyfile('config.ini.example', 'config.ini')

    config = ConfigParser.ConfigParser()
    config.read(args.config)
    channels = [[] for i in range(int(config.get('general','channels')))]
    if not 'general' in config.sections():
        raise ValueError('No general section in the config')
    
    for section in config.sections():
        if section == 'general':
            continue
        for channel in config.get(section,'channels').split(','):
            if config.get(section,'type') == 'sinwave':
               channels[int(channel)-1].append(sine_wave.generate(float(config.get(section,'frequency')), int(config.get('general','rate')), float(config.get(section,'amplitude'))))
            if config.get(section,'type') == 'white_noise':
                channels[int(channel)-1].append(white_noise.generate(config.get(section,'amplitude'),config.get(section,'seed')))


    print channels
    # each channel is defined by infinite functions which are added to produce a sample.
    #channels = ((sine_wave.generate(args.frequency, args.rate, args.amplitude),) for i in range(args.channels))

    # convert the channel functions into waveforms
    samples = sample_prep.compute_samples(channels, int(config.get('general','rate')) * int(config.get('general','length')))

    # write the samples to a file
    #if args.filename == '-':
    #    filename = sys.stdout
    #else:
    filename = args.filename
    writer.write(filename, samples, int(config.get('general','rate')) * int(config.get('general','length')), int(config.get('general','channels')), int(config.get('general','bits')) / 8, int(config.get('general','rate')))

if __name__ == "__main__":
    main()
