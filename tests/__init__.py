import os
import sys
path = os.path.dirname(os.path.abspath(''))
test_path = path + '\\tests'

sys.path.append(path)
sys.path.append(test_path)

from sdk.strategies import *