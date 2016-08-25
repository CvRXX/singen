'''          Copyright Carlos van Rooijen 2016.
 Distributed under the Boost Software License, Version 1.0.
    (See accompanying file LICENSE or copy at
          http://www.boost.org/LICENSE_1_0.txt)
'''

from itertools import *
import math

def generate(frequency=440.0, framerate=44100, amplitude=0.5):
    '''
    Generate a sine wave at a given frequency of infinite length.
    '''
    period = int(framerate / frequency)
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    lookup_table = [float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i%period)/float(framerate))) for i in xrange(period)]
    return (lookup_table[i%period] for i in count(0))

