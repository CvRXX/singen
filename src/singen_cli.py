'''          Copyright Carlos van Rooijen 2016.
 Distributed under the Boost Software License, Version 1.0.
    (See accompanying file LICENSE or copy at
          http://www.boost.org/LICENSE_1_0.txt)
'''

#!/usr/bin/env python
import argparse
import ConfigParser
import os.path
from shutil import copyfile
import collections


from wavtools import *
from generators import *

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help="The config file to be used", default='config.ini')
    parser.add_argument('filename', help="The file to generate.")
    return parser.parse_args()

def parseConfig(location):
 
    #check if a config file exists, if not, create one from the example.
    if not os.path.isfile(location):
        print("No config found, creating one...")
        copyfile('config.ini.example', 'config.ini')

    #read out the config file.
    config = ConfigParser.ConfigParser()
    config.read(location)
    
    #check if a general section excists in the config
    if not 'general' in config.sections():
        raise ValueError('No general section in the config')
    return config

def createFunctions(config):
    #where the samples will be stored.
    channels = [[] for i in range(int(config.get('general','channels')))]
    
    
    #check each section for known types and add it to the specified channels
    for section in config.sections():
        if section == 'general':
            continue
        for channel in config.get(section,'channels').split(','):
            if config.get(section,'type') == 'sinwave':
               channels[int(channel)-1].append(sine_wave.generate(float(config.get(section,'frequency')), int(config.get('general','rate')), float(config.get(section,'amplitude')),float(config.get(section,'shift'))))
            if config.get(section,'type') == 'white_noise':
                channels[int(channel)-1].append(white_noise.generate(config.get(section,'amplitude'),config.get(section,'seed')))
    return channels

def createWaves(channels, config):
    # convert the channel functions into waveforms
    return sample_prep.compute_samples(channels, int(config.get('general','rate')) * int(config.get('general','length')))

def writeToFile(samples, config, filename):
    writer.write(filename, samples, int(config.get('general','rate')) * int(config.get('general','length')), int(config.get('general','channels')), int(config.get('general','bits')) / 8, int(config.get('general','rate')))

def dumpOneWave(config):
    config = parseConfig(config)
    channels = createFunctions(config)
    return sample_prep.compute_samples(channels, int(config.get('general','rate'))/10) 


def main():
    args = parseArgs()
    config = parseConfig(args.config)
    
    channels = createFunctions(config)
    samples = createWaves(channels, config)
    

    print("Generating the file....")
    print("This could take a while.")
    
    writeToFile(samples, config, args.filename)
if __name__ == "__main__":
    main()
