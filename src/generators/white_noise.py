'''          Copyright Carlos van Rooijen 2016.
 Distributed under the Boost Software License, Version 1.0.
    (See accompanying file LICENSE or copy at
          http://www.boost.org/LICENSE_1_0.txt)
'''

from itertools import *
import random
def generate(amplitude=0.5, seed=random.random()):
    '''
    Generate random samples.
    '''
    return (float(amplitude) * random.uniform(-1, 1) for i in count(0))
