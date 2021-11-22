import sys
import time 
import os

from numpy.lib.type_check import imag
import carla
import glob
import random
import numpy as np
import cv2
import PIL
from PIL import Image, ImageFile
import matplotlib.pyplot as plt


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass



