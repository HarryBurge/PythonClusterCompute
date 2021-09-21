#~ Imports
from multiprocessing import managers
import os
from socket import socket
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
import time
from pathos.multiprocessing import Pool
from multiprocessing.managers import BaseManager

from ComputeNode import node

#~ Consts

#~ Simulation
def main():
    nodes = 